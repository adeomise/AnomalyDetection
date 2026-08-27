# Training Guide

## Verified Baseline

EXP-001 is the completed, immutable comparison baseline.

- Model: pretrained `yolov8m.pt`
- Class: `0=fire`
- Dataset: train 106 / val 31 / test 15
- Training: 50 epochs, image size 800, batch 16
- Best epoch: 46
- Precision: 0.99359
- Recall: 0.97872
- mAP50: 0.98924
- mAP50-95: 0.62694

The authoritative record, including attempts and checkpoint SHA-256, is [EXP-001-baseline.md](../experiments/EXP-001-baseline.md). Do not rerun 50 epochs as a normal onboarding or integration step.

## Supported EXP-001 Commands

Run these only in the verified Colab environment described in the [Colab guide](colab_baseline_guide.md).

```bash
# Configuration only: no credentials, dataset, model, or training
/content/baseline-env/bin/python scripts/train/run_exp001.py \
  --config configs/model/exp001-baseline.yaml \
  --dry-run

# Download and validate dataset only: no model load or training
/content/baseline-env/bin/python scripts/train/run_exp001.py \
  --config configs/model/exp001-baseline.yaml \
  --prepare-only

# Finalize an existing completed run: no dataset download, validation inference, or training
/content/baseline-env/bin/python scripts/train/run_exp001.py \
  --config configs/model/exp001-baseline.yaml \
  --finalize-run runs/detect/train2
```

Full training is an explicit experiment operation, not a quick-start requirement. It requires the verified environment, `ROBOFLOW_API_KEY`, dataset validation, and deliberate authorization by the experiment owner.

## Checkpoint Handling

The validated EXP-001 `best.pt` is not committed. Role A distributes it through the team-approved artifact channel with:

- experiment ID and model family;
- SHA-256 checksum;
- class mapping `0=fire`;
- training configuration and metrics;
- expected Ultralytics/PyTorch environment.

Consumers verify the hash before use and inject the local checkpoint path through config or CLI. See the [real-time handoff contract](realtime_guide.md).

## Follow-up Experiment Protocol

Keep EXP-001 unchanged. Each new experiment must:

1. state one primary hypothesis;
2. change one major variable at a time;
3. preserve all other baseline settings where technically possible;
4. use a new experiment ID and config;
5. record dataset provenance, environment, checkpoint hash, metrics, and decision;
6. avoid overwriting EXP-001 artifacts or records.

Candidate experiments, not yet executed:

| Candidate | Primary variable |
| --- | --- |
| EXP-002 | Hard-negative examples |
| EXP-003 | One additional fire dataset |
| EXP-004 | Fire/smoke multi-class labels |
| EXP-005 | Image size or augmentation, separated into controlled trials |
| EXP-006 | Real-time inference thresholds |

Use [experiments/README.md](../experiments/README.md) as the record template. Model improvement work remains TODO.
