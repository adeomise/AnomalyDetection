"""Run the project-side EXP-001 baseline reproduction workflow."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


EXPECTED_ULTRALYTICS = "8.0.20"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
IMAGE_SUFFIXES = {".bmp", ".jpeg", ".jpg", ".png", ".tif", ".tiff", ".webp"}
NORMALIZED_DATA_YAML = "data.exp001-normalized.yaml"
RESULTS_CSV_METRICS = {
    "precision": "metrics/precision(B)",
    "recall": "metrics/recall(B)",
    "map50": "metrics/mAP50(B)",
    "map50_95": "metrics/mAP50-95(B)",
}


def load_config(config_path: Path) -> dict[str, Any]:
    with config_path.open(encoding="utf-8") as file:
        config = yaml.safe_load(file)
    if not isinstance(config, dict):
        raise ValueError("Config must contain a mapping.")
    required = {
        "experiment_id",
        "model",
        "training",
        "dataset",
        "classes",
    }
    missing = required.difference(config)
    if missing:
        raise ValueError(f"Missing config fields: {', '.join(sorted(missing))}")
    return config


def verify_class_mapping(config: dict[str, Any], data_yaml: Path) -> dict[str, Any]:
    with data_yaml.open(encoding="utf-8") as file:
        dataset = yaml.safe_load(file)
    names = dataset.get("names") if isinstance(dataset, dict) else None
    if isinstance(names, list):
        names = {index: value for index, value in enumerate(names)}
    if not isinstance(names, dict):
        raise ValueError("data.yaml must define class names.")
    normalized = {int(key): str(value) for key, value in names.items()}
    if normalized.get(0) != "fire":
        raise ValueError(f"Expected class 0 to be fire; found {normalized.get(0)!r}.")
    configured = {int(key): str(value) for key, value in config["classes"].items()}
    if configured != normalized:
        raise ValueError(f"Config classes {configured} do not match data.yaml classes {normalized}.")
    return dataset


def resolve_path(value: str, data_yaml: Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else data_yaml.parent / path


def validate_dataset(data_yaml: Path, config: dict[str, Any]) -> dict[str, Any]:
    if not data_yaml.is_file():
        raise FileNotFoundError(f"data.yaml does not exist: {data_yaml}")
    dataset = verify_class_mapping(config, data_yaml)
    if "train" not in dataset:
        raise ValueError("data.yaml does not define train.")
    validation_key = "val" if "val" in dataset else "valid" if "valid" in dataset else None
    if validation_key is None:
        raise ValueError("data.yaml must define val or valid.")
    for key in ("train", validation_key, "test"):
        if key not in dataset:
            if key == "test":
                continue
            raise ValueError(f"data.yaml does not define {key}.")
        split_path = resolve_path(str(dataset[key]), data_yaml)
        if not split_path.exists():
            raise FileNotFoundError(f"Dataset {key} path does not exist: {split_path}")
    return dataset


def verify_labels(dataset: dict[str, Any], data_yaml: Path) -> None:
    train_path = resolve_path(str(dataset["train"]), data_yaml)
    labels_root = train_path.parent / "labels" if train_path.name == "images" else train_path / "labels"
    if not labels_root.is_dir():
        raise FileNotFoundError(f"Training labels directory does not exist: {labels_root}")
    sample = next(labels_root.glob("*.txt"), None)
    if sample is None:
        raise ValueError(f"No training label sample found in {labels_root}")
    for line_number, line in enumerate(sample.read_text(encoding="utf-8").splitlines(), 1):
        fields = line.split()
        if len(fields) != 5:
            raise ValueError(f"Invalid label fields in {sample}:{line_number}")
        class_id, *coordinates = fields
        if int(class_id) != 0 or any(not 0 <= float(value) <= 1 for value in coordinates):
            raise ValueError(f"Invalid normalized label in {sample}:{line_number}")


def validate_label_file(label_path: Path) -> None:
    for line_number, line in enumerate(label_path.read_text(encoding="utf-8").splitlines(), 1):
        fields = line.split()
        if len(fields) != 5:
            raise ValueError(f"Invalid YOLO label fields in {label_path}:{line_number}; expected 5.")
        try:
            class_id = int(fields[0])
            coordinates = [float(value) for value in fields[1:]]
        except ValueError as exc:
            raise ValueError(f"Non-numeric YOLO label in {label_path}:{line_number}.") from exc
        if class_id != 0:
            raise ValueError(f"Expected class 0 in {label_path}:{line_number}; found {class_id}.")
        if any(value < 0 or value > 1 for value in coordinates):
            raise ValueError(f"Coordinates are outside [0, 1] in {label_path}:{line_number}.")


def validate_split(split_name: str, images_root: Path) -> tuple[int, int]:
    if not images_root.is_dir():
        raise FileNotFoundError(f"Dataset {split_name} image directory does not exist: {images_root}")
    labels_root = images_root.parent / "labels" if images_root.name == "images" else images_root / "labels"
    if not labels_root.is_dir():
        raise FileNotFoundError(f"Dataset {split_name} label directory does not exist: {labels_root}")

    image_files = sorted(path for path in images_root.rglob("*") if path.suffix.lower() in IMAGE_SUFFIXES)
    label_files = sorted(labels_root.rglob("*.txt"))
    if not image_files:
        raise ValueError(f"No images found in {images_root}")
    if not label_files:
        raise ValueError(f"No labels found in {labels_root}")
    for label_path in label_files:
        validate_label_file(label_path)

    print(f"{split_name}: images={len(image_files)}, labels={len(label_files)}")
    return len(image_files), len(label_files)


def validate_prepared_dataset(data_yaml: Path, config: dict[str, Any]) -> None:
    dataset = validate_dataset(data_yaml, config)
    validation_key = "val" if "val" in dataset else "valid"
    split_keys = ["train", validation_key]
    if "test" in dataset:
        split_keys.append("test")
    for split_name in split_keys:
        validate_split(split_name, resolve_path(str(dataset[split_name]), data_yaml))


def normalize_data_yaml(dataset_root: Path, config: dict[str, Any]) -> Path:
    dataset_root = dataset_root.resolve()
    source_yaml = dataset_root / "data.yaml"
    source = verify_class_mapping(config, source_yaml)
    if "train" not in source:
        raise ValueError("Original data.yaml does not define train.")
    if "val" not in source and "valid" not in source:
        raise ValueError("Original data.yaml must define val or valid.")

    train_images = dataset_root / "train" / "images"
    validation_candidates = (dataset_root / "valid" / "images", dataset_root / "val" / "images")
    validation_images = next((path for path in validation_candidates if path.is_dir()), None)
    if not train_images.is_dir():
        raise FileNotFoundError(f"Dataset train image directory does not exist: {train_images}")
    if validation_images is None:
        raise FileNotFoundError(
            f"Dataset validation image directory does not exist: {validation_candidates[0]} or {validation_candidates[1]}"
        )

    normalized = dict(source)
    normalized.pop("valid", None)
    normalized["train"] = str(train_images.resolve())
    normalized["val"] = str(validation_images.resolve())
    if "test" in source:
        test_images = dataset_root / "test" / "images"
        if not test_images.is_dir():
            raise FileNotFoundError(f"Dataset test image directory does not exist: {test_images}")
        normalized["test"] = str(test_images.resolve())

    normalized_yaml = dataset_root / NORMALIZED_DATA_YAML
    normalized_yaml.write_text(yaml.safe_dump(normalized, sort_keys=False), encoding="utf-8")
    return normalized_yaml


def download_dataset(config: dict[str, Any], api_key: str) -> Path:
    from roboflow import Roboflow

    dataset_config = config["dataset"]
    dataset = (
        Roboflow(api_key=api_key)
        .workspace(dataset_config["workspace"])
        .project(dataset_config["project"])
        .version(dataset_config["version"])
        .download(dataset_config["format"])
    )
    return Path(dataset.location)


def run_verification() -> None:
    script = PROJECT_ROOT / "scripts" / "colab" / "verify_exp001.py"
    subprocess.run([sys.executable, str(script)], check=True)


def file_metadata(path: Path) -> dict[str, Any]:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return {"path": str(path), "size_bytes": path.stat().st_size, "sha256": digest}


def collect_training_outputs(model: Any) -> tuple[Path, dict[str, float]]:
    trainer = getattr(model, "trainer", None)
    if trainer is None:
        raise RuntimeError("Ultralytics trainer state is unavailable after training.")

    save_dir = Path(trainer.save_dir)
    best_path = Path(getattr(trainer, "best", save_dir / "weights" / "best.pt"))
    if not best_path.is_file():
        raise FileNotFoundError(f"Training completed without best.pt: {best_path}")

    trainer_metrics = getattr(trainer, "metrics", None)
    if not isinstance(trainer_metrics, dict):
        raise RuntimeError("Ultralytics trainer metrics are unavailable after final validation.")
    missing = [source for source in RESULTS_CSV_METRICS.values() if source not in trainer_metrics]
    if missing:
        raise RuntimeError(f"Ultralytics trainer metrics are missing: {', '.join(missing)}")
    metrics = {name: float(trainer_metrics[source]) for name, source in RESULTS_CSV_METRICS.items()}
    return best_path, metrics


def read_best_csv_metrics(results_csv: Path) -> tuple[int, dict[str, float]]:
    if not results_csv.is_file():
        raise FileNotFoundError(f"Ultralytics results.csv does not exist: {results_csv}")
    with results_csv.open(encoding="utf-8", newline="") as file:
        rows = [{key.strip(): value.strip() for key, value in row.items()} for row in csv.DictReader(file)]
    required = {"epoch", *RESULTS_CSV_METRICS.values()}
    if not rows:
        raise ValueError(f"Ultralytics results.csv contains no metric rows: {results_csv}")
    missing = required.difference(rows[0])
    if missing:
        raise ValueError(f"Ultralytics results.csv is missing columns: {', '.join(sorted(missing))}")

    candidates: list[tuple[float, int, dict[str, float]]] = []
    for row_number, row in enumerate(rows, 2):
        try:
            epoch = int(float(row["epoch"]))
            metrics = {name: float(row[column]) for name, column in RESULTS_CSV_METRICS.items()}
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid numeric metric in {results_csv}:{row_number}") from exc
        if not all(math.isfinite(value) for value in metrics.values()):
            raise ValueError(f"Non-finite metric in {results_csv}:{row_number}")
        fitness = 0.1 * metrics["map50"] + 0.9 * metrics["map50_95"]
        candidates.append((fitness, epoch, metrics))
    _, best_epoch, best_metrics = max(candidates, key=lambda candidate: (candidate[0], candidate[1]))
    return best_epoch, best_metrics


def write_result(summary: dict[str, Any]) -> Path:
    result_path = PROJECT_ROOT / "artifacts" / "exp001" / "result.json"
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(summary, indent=2, default=float), encoding="utf-8")
    print(json.dumps(summary, indent=2, default=float))
    return result_path


def finalize_run(run_dir: Path, config: dict[str, Any], config_path: Path) -> None:
    run_dir = (run_dir if run_dir.is_absolute() else PROJECT_ROOT / run_dir).resolve()
    if not run_dir.is_dir():
        raise FileNotFoundError(f"Ultralytics run directory does not exist: {run_dir}")
    best_path = run_dir / "weights" / "best.pt"
    if not best_path.is_file():
        raise FileNotFoundError(f"Ultralytics best.pt does not exist: {best_path}")
    results_csv = run_dir / "results.csv"
    best_epoch, metrics = read_best_csv_metrics(results_csv)
    summary = {
        "experiment_id": config["experiment_id"],
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "run_dir": str(run_dir),
        "best_pt": file_metadata(best_path),
        "metrics": metrics,
        "metrics_source": {
            "path": str(results_csv),
            "selected_epoch_index": best_epoch,
            "selected_epoch_number": best_epoch + 1,
            "selection": "Ultralytics 8.0.20 fitness: 0.1*mAP50 + 0.9*mAP50-95",
        },
        "provenance": {
            "config": file_metadata(config_path),
            "dataset": config["dataset"],
            "classes": config["classes"],
            "training": config["training"],
            "model": config["model"],
        },
    }
    write_result(summary)


def dry_run(config: dict[str, Any], config_path: Path) -> None:
    print("EXP-001 dry-run: PASS")
    print(json.dumps({"config": str(config_path), "planned": config}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--prepare-only", action="store_true")
    mode.add_argument("--finalize-run", type=Path)
    args = parser.parse_args()
    config_path = args.config if args.config.is_absolute() else PROJECT_ROOT / args.config
    config = load_config(config_path)
    if args.dry_run:
        dry_run(config, config_path)
        return
    if args.finalize_run is not None:
        finalize_run(args.finalize_run, config, config_path)
        return

    run_verification()
    api_key = os.environ.get("ROBOFLOW_API_KEY")
    if not api_key:
        raise RuntimeError("ROBOFLOW_API_KEY is not set; training is stopped.")

    dataset_root = download_dataset(config, api_key)
    data_yaml = normalize_data_yaml(dataset_root, config)
    if args.prepare_only:
        validate_prepared_dataset(data_yaml, config)
        print("Dataset location:", dataset_root.resolve())
        print("Normalized data.yaml:", data_yaml)
        print("EXP-001 dataset preparation: PASS")
        return

    from ultralytics import YOLO, __version__

    if __version__ != EXPECTED_ULTRALYTICS:
        raise RuntimeError(f"Ultralytics {EXPECTED_ULTRALYTICS} is required; found {__version__}.")
    dataset_config = config["dataset"]
    dataset_values = validate_dataset(data_yaml, config)
    verify_labels(dataset_values, data_yaml)

    training = config["training"]
    model_path = config["model"]["pretrained"]
    model = YOLO(model_path)
    model.train(data=str(data_yaml), **training)
    best_path, metrics = collect_training_outputs(model)
    summary = {
        "experiment_id": config["experiment_id"],
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "dataset_version": dataset_config["version"],
        "python": sys.version,
        "pytorch": __import__("torch").__version__,
        "ultralytics": __version__,
        "gpu": __import__("torch").cuda.get_device_name(0),
        "best_pt": file_metadata(best_path),
        "metrics": metrics,
    }
    write_result(summary)


if __name__ == "__main__":
    main()
