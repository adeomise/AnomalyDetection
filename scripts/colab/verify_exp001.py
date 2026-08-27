"""Verify the isolated EXP-001 training environment."""

from __future__ import annotations

import importlib
import platform
import sys


EXPECTED_PYTHON = (3, 10)
EXPECTED_ULTRALYTICS = "8.0.20"


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
    except ImportError:
        fail("PyTorch is not installed.")

    print("PyTorch version:", torch.__version__)
    print("torch CUDA build:", torch.version.cuda)
    print("torch.cuda.is_available():", torch.cuda.is_available())
    if not torch.cuda.is_available():
        fail("CUDA is unavailable; training is stopped.")

    gpu_name = torch.cuda.get_device_name(0)
    print("GPU name:", gpu_name)

    try:
        ultralytics = importlib.import_module("ultralytics")
    except ImportError:
        fail("Ultralytics is not installed.")

    print("Ultralytics version:", ultralytics.__version__)
    if ultralytics.__version__ != EXPECTED_ULTRALYTICS:
        fail(f"Ultralytics {EXPECTED_ULTRALYTICS} is required; found {ultralytics.__version__}.")

    try:
        importlib.import_module("roboflow")
    except ImportError:
        fail("Roboflow is not importable.")
    print("Roboflow import: available")
    print("environment verification: PASS")


if __name__ == "__main__":
    main()