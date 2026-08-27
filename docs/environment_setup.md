# Environment Setup

This document separates the environment observed in upstream notebook outputs from the current Windows machine. No package was installed and no system CUDA, driver, or global Python setting was changed during this investigation.

## Current PC

- OS: Windows (workspace environment)
- Installed Python versions: 3.9, 3.11, 3.12, 3.14
- Default `py` interpreter: Python 3.14.2 at `C:\Users\adeom\AppData\Local\Programs\Python\Python314\python.exe`
- VS Code configured interpreter inspected for this workspace: Python 3.14.5 at `C:\Users\adeom\AppData\Local\Python\pythoncore-3.14-64\python.exe`
- Configured interpreter pip: 26.1.1
- `nvidia-smi`: Not available on PATH
- `nvcc`: Not available on PATH
- PyTorch in configured interpreter: Not installed
- Ultralytics, Roboflow, Supervision, OpenCV, NumPy, YOLOX, onemetric, and tqdm in configured interpreter: Not installed

The `nvidia-smi` and `nvcc` results do not prove that no GPU or driver exists; they only show that these commands were unavailable through the current PATH. No driver or CUDA change was attempted.

## Upstream Environment Evidence

The following values are saved output from the pinned upstream notebooks, not independently reproduced values on this PC:

- Notebook: `drone_fire_detection_yolov8.ipynb`
- Python: `3.10.12`
- PyTorch: `2.0.1+cu118`
- PyTorch CUDA build: `cu118`
- GPU: NVIDIA Tesla T4, 15102 MiB
- NVIDIA driver: `525.105.17`
- `nvidia-smi` reported CUDA compatibility: `12.0`
- Ultralytics: `YOLOv8.0.20`
- Recorded setup: 2 CPUs, 12.7 GB RAM

The video inference notebook separately records Ultralytics `8.0.168`, Python `3.10.12`, torch `2.0.1+cu118`, Tesla T4, driver `525.105.17`, and `supervision==0.1.0` / YOLOX `0.1.0`. This is an inference notebook environment and must not silently replace the training notebook's pinned `ultralytics==8.0.20`.

## Dependency Matrix

| Component | Upstream evidence | Current system | EXP-001 status |
| --- | --- | --- | --- |
| Python | `3.10.12` in saved notebook output; original requirement not declared | 3.9, 3.11, 3.12, 3.14 installed; configured interpreter 3.14.5 | Candidate required; not selected |
| PyTorch | `2.0.1+cu118` in saved notebook output | Not installed in configured interpreter | Candidate required; compatibility not yet verified |
| CUDA | PyTorch build `cu118`; `nvidia-smi` output reported compatibility `12.0` | `nvidia-smi` and `nvcc` unavailable on PATH | Pending local GPU/driver verification |
| cuDNN | Not specified | Not inspected | Not specified upstream |
| Ultralytics | `8.0.20` explicitly installed in training notebook | Not installed | Confirmed upstream training value; local install pending |
| Roboflow | Installed without version in training notebook | Not installed | Required for dataset acquisition; version pending |
| Supervision | `0.1.0` explicitly installed in video inference notebook; image notebook unpinned | Not installed | Not required for initial training |
| OpenCV (`cv2`) | Imported in image inference notebook; install/version not specified | Not installed | Not required by training notebook evidence |
| NumPy | Imported in video inference notebook; version not specified | Not installed | Required by inference code; not required for initial training plan |
| YOLOX / ByteTrack dependencies | `yolox==0.1.0` output; ByteTrack setup installs `cython_bbox`, `onemetric`, `loguru`, `lap`, `thop` | Not installed | Not required for initial training |

Status meanings: `Confirmed` is directly supported by a source; `Candidate` is a reproduction choice not yet validated; `Pending` requires more local evidence; `Not required for initial training` applies only to the first EXP-001 training environment.

## Reproduction Environment Candidate

- Python: Candidate only - Python 3.10.x is suggested by the upstream saved output, but no local Python 3.10 installation was found and compatibility is not yet verified.
- PyTorch: Candidate only - `2.0.1+cu118`, matching the upstream saved output; package availability and compatibility on this Windows machine are not verified.
- CUDA strategy: Candidate only - use a PyTorch CUDA build matching the selected PyTorch package; do not equate `nvidia-smi` CUDA compatibility with an installed Toolkit.
- Ultralytics: Confirmed upstream training value `8.0.20`; local installation pending.
- Roboflow: Required, version not specified upstream; select and record only after compatibility verification.
- Environment location: Planned isolated `C:\AnomalyDetection\.venv-baseline`; not created in this step.
- Reason: Preserve the upstream training stack as closely as possible while isolating it from global Python and future project dependencies.

No candidate is approved for training yet. The candidate values must be validated before environment creation.

## Required for EXP-001 Training

- Python runtime
- PyTorch and a verified CPU/GPU execution strategy
- Ultralytics `8.0.20`
- Roboflow client and access to project version 1
- The exported dataset and its `data.yaml`
- `yolov8m.pt` source

## Not Required for Initial EXP-001 Training

Based on the upstream notebooks, these belong to later inference or video annotation work and should remain outside the initial training environment unless a dependency check proves otherwise:

- Supervision
- ByteTrack / YOLOX packages
- `cython_bbox`, `onemetric`, `loguru`, `lap`, and `thop`
- Video annotation dependencies

## Compatibility Risks

### Confirmed observations

- The training notebook explicitly installs the old `ultralytics==8.0.20`.
- The saved upstream runtime used Python 3.10.12 and torch 2.0.1 with CUDA 11.8 build.
- The current configured Python is 3.14.5 and does not have PyTorch or upstream packages installed.
- Upstream notebook paths use Google Colab paths such as `/content`.

### Potential compatibility risks

- Older Ultralytics and PyTorch packages may not provide compatible wheels for Python 3.14.
- A PyTorch `cu118` build does not require the local CUDA Toolkit, but it does require a compatible NVIDIA driver at runtime.
- `nvidia-smi` CUDA Version describes driver compatibility, not necessarily the installed CUDA Toolkit version.
- NumPy, Roboflow, Supervision, and ByteTrack package APIs may differ from the 2023 notebook environment.
- The notebook's ByteTrack setup edits a cloned dependency's requirements with `sed`, which is not a native Windows workflow; it is not part of initial training.
- Colab-specific paths, API key handling, and automatic weight download need project-side treatment later; upstream notebooks remain unchanged.

## EXP-001 Environment Checklist

- [ ] Python reproduction version selected
- [ ] Isolated virtual environment created
- [ ] PyTorch version selected
- [ ] GPU available from PyTorch
- [ ] Ultralytics 8.0.20 installed
- [ ] Roboflow client available
- [ ] Dataset version 1 downloaded
- [ ] `data.yaml` inspected
- [ ] train/valid/test split verified
- [ ] Class ID verified
- [ ] `yolov8m.pt` source confirmed
- [x] Upstream code remains unchanged

## Status

Current status: **Not Ready**

## Initial Colab Automation Test

- Python 3.10.21 provisioning succeeded.
- torch 2.0.1+cu118 was initially installed.
- Later dependency resolution upgraded torch to 2.13.0+cu130.
- ultralytics 8.0.20 import failed because pkg_resources was unavailable.
- Verification correctly returned FAIL.
- Training was not executed.

The EXP-001 automation now constrains every install to torch `2.0.1+cu118`, torchvision `0.15.2+cu118`, NumPy `1.26.4`, Ultralytics `8.0.20`, and setuptools `<82`. The torch/torchvision pair is the official PyTorch CUDA 11.8 wheel combination for PyTorch 2.0.1. NumPy stays on 1.x because NumPy 2.0 introduced an ABI break for extensions compiled against NumPy 1.x. Setuptools stays below 82 because version 82 removed `pkg_resources` from distributions.

Ready for environment creation requires a selected Python candidate, a PyTorch/CUDA strategy, and a documented dependency plan. Ready for training additionally requires the isolated environment, package checks, dataset inspection, class verification, split verification, and pretrained weight source confirmation. Training is intentionally not performed in this step.

TODO: After the candidate is approved, create the isolated environment and record its exact package resolution in a separate environment artifact. Do not put unverified versions into the root `requirements.txt`.
