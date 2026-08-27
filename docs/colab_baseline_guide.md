# EXP-001 Colab Baseline Guide

EXP-001 is complete. This guide documents reproducibility and artifact inspection; normal participant onboarding does not require another 50-epoch run.

## Runtime and Secret

1. Clone this repository at `/content/AnomalyDetection`.
2. Select a Colab GPU runtime.
3. Add a Colab Secret named `ROBOFLOW_API_KEY` only when dataset preparation or full training is explicitly required. Never print or save it.

## Setup and Verification

```bash
cd /content/AnomalyDetection
bash scripts/colab/setup_exp001.sh
```

Stop unless setup prints both `environment verification: PASS` and `Environment setup: PASS`. Exact versions and checks are documented in [environment_setup.md](environment_setup.md).

## Safe Workflow Modes

```bash
# Config inspection only
/content/baseline-env/bin/python scripts/train/run_exp001.py \
  --config configs/model/exp001-baseline.yaml --dry-run

# Dataset download and validation only; requires ROBOFLOW_API_KEY
/content/baseline-env/bin/python scripts/train/run_exp001.py \
  --config configs/model/exp001-baseline.yaml --prepare-only

# Finalize an existing run without training or validation inference
/content/baseline-env/bin/python scripts/train/run_exp001.py \
  --config configs/model/exp001-baseline.yaml \
  --finalize-run runs/detect/train2
```

Full training is intentionally omitted from quick start. Run it only under an approved new reproduction task.

## Verified Outputs

- normalized dataset YAML: `<dataset.location>/data.exp001-normalized.yaml`;
- local run directory: Ultralytics `runs/detect/<run-name>/`;
- checkpoint: `weights/best.pt`, distributed outside Git;
- summary: `artifacts/exp001/result.json`;
- authoritative metrics/checksum: [EXP-001-baseline.md](../experiments/EXP-001-baseline.md).

## Project / Upstream Boundary

The launcher, constraints, validation, and result finalization are project-side automation. The external `tim3in/Fire-Detection-Drone` source remains a read-only provenance reference and is not represented as project-owned code.
