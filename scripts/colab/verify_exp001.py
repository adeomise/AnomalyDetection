"""Verify the isolated EXP-001 training environment."""

from __future__ import annotations

import importlib
import importlib.metadata
import platform
import sys


EXPECTED_PYTHON = (3, 10)
EXPECTED_TORCH = "2.0.1+cu118"
EXPECTED_TORCHVISION = "0.15.2+cu118"
EXPECTED_TORCH_CUDA = "11.8"
EXPECTED_ULTRALYTICS = "8.0.20"
EXPECTED_NUMPY = "1.26.4"
EXPECTED_ROBOFLOW = "1.4.1"
EXPECTED_PYTHON_DOTENV = "1.2.3"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    print("environment verification: FAIL")
    raise SystemExit(1)


def main() -> None:
    print("Python version:", platform.python_version())
    print("Python executable:", sys.executable)

    if sys.version_info[:2] != EXPECTED_PYTHON:
        fail("Python 3.10 is required for EXP-001.")

    try:
        torch = importlib.import_module("torch")
    except Exception as exc:
        fail(f"PyTorch is not importable: {exc}")

    print("PyTorch version:", torch.__version__)
    print("torch CUDA build:", torch.version.cuda)
    if torch.__version__ != EXPECTED_TORCH:
        fail(f"PyTorch {EXPECTED_TORCH} is required; found {torch.__version__}.")
    if torch.version.cuda != EXPECTED_TORCH_CUDA:
        fail(f"PyTorch CUDA build {EXPECTED_TORCH_CUDA} is required; found {torch.version.cuda}.")

    try:
        torchvision = importlib.import_module("torchvision")
    except Exception as exc:
        fail(f"Torchvision is not importable: {exc}")
    print("Torchvision version:", torchvision.__version__)
    if torchvision.__version__ != EXPECTED_TORCHVISION:
        fail(f"Torchvision {EXPECTED_TORCHVISION} is required; found {torchvision.__version__}.")

    try:
        numpy = importlib.import_module("numpy")
    except Exception as exc:
        fail(f"NumPy is not importable: {exc}")
    print("NumPy version:", numpy.__version__)
    if numpy.__version__ != EXPECTED_NUMPY:
        fail(f"NumPy {EXPECTED_NUMPY} is required; found {numpy.__version__}.")

    try:
        importlib.import_module("pkg_resources")
    except Exception as exc:
        fail(f"pkg_resources is not importable: {exc}")
    print("pkg_resources import: available")

    print("torch.cuda.is_available():", torch.cuda.is_available())
    if not torch.cuda.is_available():
        fail("CUDA is unavailable; training is stopped.")

    gpu_name = torch.cuda.get_device_name(0)
    print("GPU name:", gpu_name)

    try:
        ultralytics = importlib.import_module("ultralytics")
    except Exception as exc:
        fail(f"Ultralytics is not importable: {exc}")

    print("Ultralytics version:", ultralytics.__version__)
    if ultralytics.__version__ != EXPECTED_ULTRALYTICS:
        fail(f"Ultralytics {EXPECTED_ULTRALYTICS} is required; found {ultralytics.__version__}.")

    try:
        importlib.import_module("roboflow")
    except Exception as exc:
        fail(f"Roboflow is not importable: {exc}")
    print("Roboflow import: available")

    try:
        roboflow_version = importlib.metadata.version("roboflow")
    except importlib.metadata.PackageNotFoundError:
        fail("Roboflow distribution metadata is unavailable.")
    print("Roboflow version:", roboflow_version)
    if roboflow_version != EXPECTED_ROBOFLOW:
        fail(f"Roboflow {EXPECTED_ROBOFLOW} is required; found {roboflow_version}.")

    try:
        importlib.import_module("dotenv")
    except Exception as exc:
        fail(f"dotenv is not importable: {exc}")
    print("dotenv import: available")

    try:
        python_dotenv_version = importlib.metadata.version("python-dotenv")
    except importlib.metadata.PackageNotFoundError:
        fail("python-dotenv distribution metadata is unavailable.")
    print("python-dotenv version:", python_dotenv_version)
    if python_dotenv_version != EXPECTED_PYTHON_DOTENV:
        fail(f"python-dotenv {EXPECTED_PYTHON_DOTENV} is required; found {python_dotenv_version}.")

    print("environment verification: PASS")


if __name__ == "__main__":
    main()
