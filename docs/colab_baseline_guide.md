# EXP-001 Colab Baseline Guide

This guide runs the project-side reproduction launcher for the pinned `tim3in/Fire-Detection-Drone` baseline. It does not modify or execute the upstream notebooks.

## 1. Open the Notebook

Open `colab/EXP-001-baseline.ipynb` in Google Colab from the project repository. The notebook expects the repository at `/content/AnomalyDetection`. If using a new Colab runtime, clone this repository into that path before running the launcher cells.

## 2. Select a GPU Runtime

In Colab, select a GPU runtime before running setup. The verifier stops if PyTorch cannot see CUDA or a GPU. The upstream saved training output used a Tesla T4, but the current runtime GPU may differ.

## 3. Configure the Roboflow Secret

Add a Colab Secret named `ROBOFLOW_API_KEY` and enable notebook access. The notebook passes the secret through an environment variable. The key is never printed, written to a result file, or committed.

## 4. Run Setup

Run the setup cell. `scripts/colab/setup_exp001.sh`:

- Requires Linux/Colab
- Installs `uv` only in the Colab runtime if needed
- Creates `/content/baseline-env` with Python 3.10
- Installs the pinned PyTorch CUDA build candidate and `ultralytics==8.0.20`
- Installs Roboflow without selecting an upstream-unspecified version
- Does not fall back to latest Ultralytics or PyTorch

The PyTorch `2.0.1` and CUDA 11.8 index choice follows the saved upstream runtime evidence (`torch 2.0.1+cu118`). It remains a candidate until setup succeeds in the target Colab runtime.

## 5. Confirm Verification PASS

The verification cell must print `environment verification: PASS`. It checks:

- Python major/minor is 3.10
- PyTorch imports
- CUDA is available
- A GPU is detected
- Ultralytics is exactly 8.0.20
- Roboflow imports

Any failure stops the workflow. No training starts after a failed verification.

## 6. Run EXP-001

Run the training cell only after verification passes. The launcher loads `configs/model/exp001-baseline.yaml`, obtains Roboflow project `tim-4ijf0`, version 1, validates `data.yaml`, checks class 0 is `fire`, validates a training YOLO label sample, and then invokes the upstream conditions:

- Model: `yolov8m.pt`
- Epochs: 50
- Image size: 800
- Batch: 16
- Patience: 50
- Workers: 8

Training is intentionally not run by this repository change. It is performed only when the user executes the training cell in Colab.

## 7. Result Location

After successful training and validation, the launcher writes a machine-readable summary to `artifacts/exp001/result.json` and prints the `best.pt` path, SHA-256, environment information, and validation metrics. Model weights and artifacts are ignored by Git.

## 8. Dry Run

Before any dataset/model access, validate the config with:

```bash
/content/baseline-env/bin/python scripts/train/run_exp001.py --config configs/model/exp001-baseline.yaml --dry-run
```

Dry-run only parses and prints the planned configuration. It does not access Roboflow, download data or weights, validate a dataset, or train.

## Common Errors

- `Python 3.10 is required`: the isolated environment was not created or the wrong interpreter was used. Do not use the Colab default Python kernel for baseline commands.
- `CUDA is unavailable`: select a GPU runtime and rerun setup. Do not continue to training.
- `Ultralytics 8.0.20 is required`: setup must fail rather than install a newer version.
- `ROBOFLOW_API_KEY is not set`: configure the Colab Secret and rerun the secret cell. Never paste the key into notebook source.
- `data.yaml does not exist`: the Roboflow export did not complete or its layout differs from the expected export. Stop and inspect the dataset before training.
- `Expected class 0 to be fire`: the downloaded YAML does not match the baseline config. Stop; do not change the class mapping for EXP-001.
- `Training labels directory does not exist` or invalid label error: stop and resolve the dataset export structure; do not bypass validation.
- `sed` or ByteTrack errors: those belong to the upstream video inference notebook and are not part of initial EXP-001 training.

## Upstream and Project Boundary

Upstream repository: `tim3in/Fire-Detection-Drone`, commit `e90632a25a07ea1f2137681741e3d9bfc8f1cb3c`.

The upstream notebooks remain read-only. This repository provides an independent reproduction launcher with config externalization, secret handling, environment verification, dataset validation, and result logging. These project-side changes are not upstream modifications.

Current status: Automation prepared. Training not run.
