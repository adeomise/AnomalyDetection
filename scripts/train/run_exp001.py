"""Run the project-side EXP-001 baseline reproduction workflow."""

from __future__ import annotations

import argparse
import hashlib
import json
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
    return Path(dataset.location) / "data.yaml"


def run_verification() -> None:
    script = PROJECT_ROOT / "scripts" / "colab" / "verify_exp001.py"
    subprocess.run([sys.executable, str(script)], check=True)


def file_metadata(path: Path) -> dict[str, Any]:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return {"path": str(path), "size_bytes": path.stat().st_size, "sha256": digest}


def dry_run(config: dict[str, Any], config_path: Path) -> None:
    print("EXP-001 dry-run: PASS")
    print(json.dumps({"config": str(config_path), "planned": config}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    config_path = args.config if args.config.is_absolute() else PROJECT_ROOT / args.config
    config = load_config(config_path)
    if args.dry_run:
        dry_run(config, config_path)
        return

    run_verification()
    api_key = os.environ.get("ROBOFLOW_API_KEY")
    if not api_key:
        raise RuntimeError("ROBOFLOW_API_KEY is not set; training is stopped.")

    data_yaml = download_dataset(config, api_key)
    if args.prepare_only:
        validate_prepared_dataset(data_yaml, config)
        print("Dataset location:", data_yaml.parent)
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
    results = model.train(data=str(data_yaml), **training)
    best_path = Path(results.save_dir) / "weights" / "best.pt"
    if not best_path.is_file():
        raise FileNotFoundError(f"Training completed without best.pt: {best_path}")
    metrics = model.val(data=str(data_yaml))
    summary = {
        "experiment_id": config["experiment_id"],
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "dataset_version": dataset_config["version"],
        "python": sys.version,
        "pytorch": __import__("torch").__version__,
        "ultralytics": __version__,
        "gpu": __import__("torch").cuda.get_device_name(0),
        "best_pt": file_metadata(best_path),
        "metrics": {name: getattr(metrics.box, name, None) for name in ("mp", "mr", "map50", "map")},
    }
    result_path = PROJECT_ROOT / "artifacts" / "exp001" / "result.json"
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(summary, indent=2, default=float), encoding="utf-8")
    print(json.dumps(summary, indent=2, default=float))


if __name__ == "__main__":
    main()
