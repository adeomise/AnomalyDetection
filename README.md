# Real-time Fire Detection

## Project Overview

This project detects fire in drone or smartphone video on a laptop. The target pipeline is:

```text
Drone / smartphone video -> laptop OpenCV capture -> YOLO inference
                         -> bounding boxes + confidence + FPS / latency
```

The one-class YOLOv8 baseline, EXP-001, has been reproduced and verified in a clean Google Colab environment. Dataset preparation, training, best-checkpoint selection, validation, and result finalization are complete. The real-time OpenCV/streaming application is the next integration stage and is not implemented yet.

## Current Baseline

| Item | EXP-001 value |
| --- | --- |
| Model | Pretrained YOLOv8m (`yolov8m.pt`) |
| Classes | `0: fire` |
| Dataset | train 106 / val 31 / test 15 |
| Training | 50 epochs, image size 800, batch 16 |
| Best epoch | 46 |
| Precision | 0.99359 |
| Recall | 0.97872 |
| mAP50 | 0.98924 |
| mAP50-95 | 0.62694 |

The validated `best.pt` SHA-256 is:

```text
7b1fe847ea81bf5cd3647da1d457510b4a87d956be9eed4ab61c92db817f5ef2
```

The checkpoint itself is not stored in Git. Transfer it through the team-approved artifact channel, verify its SHA-256 after transfer, and inject its local path through configuration or a CLI argument. See [EXP-001 results](experiments/EXP-001-baseline.md) and the [training guide](docs/training_guide.md).

## Repository Structure

| Path | Role |
| --- | --- |
| `configs/` | Versioned model, environment, data, and inference settings |
| `scripts/colab/` | Verified EXP-001 Colab environment setup and verification |
| `scripts/train/` | Dataset preparation, baseline training, and run finalization entry points |
| `scripts/realtime/` | Reserved user-facing real-time entry points; implementation TODO |
| `src/` | Project-owned data, training, inference, streaming, evaluation, and utility modules |
| `data/` | Local raw/intermediate/processed/split data locations; large data is ignored |
| `models/` | Local pretrained/checkpoint locations; weights are ignored |
| `experiments/` | Immutable experiment intent, configuration, attempts, and final results |
| `colab/` | Participant starter and EXP-001 reproduction notebooks |
| `docs/` | Environment, data, training, real-time, validation, architecture, and attribution guides |
| `external/` | External-source provenance records; upstream code is not project-owned code |
| `tests/` | Automated tests as integration components are implemented |
| `assets/` | Small documentation and demo assets only |

Colab notebooks:

- Participant starter: [`colab/participant-baseline.ipynb`](colab/participant-baseline.ipynb)
- EXP-001 reproduction: [`colab/EXP-001-baseline.ipynb`](colab/EXP-001-baseline.ipynb)

## Quick Start

The default onboarding path does not retrain EXP-001.

1. Clone the repository and enter it.

   ```bash
   git clone <team-repository-url> AnomalyDetection
   cd AnomalyDetection
   ```

2. Read the completed [EXP-001 record](experiments/EXP-001-baseline.md), then review the [architecture](docs/architecture.md) and your role below.
3. For baseline environment or reproducibility work, follow the [environment setup](docs/environment_setup.md) and [Colab baseline guide](docs/colab_baseline_guide.md). Start with `--dry-run` or `--prepare-only`; do not default to 50-epoch training.
4. For model integration, obtain the validated checkpoint outside Git, verify its SHA-256, and configure its local path.
5. For real-time work, follow the [real-time guide](docs/realtime_guide.md). The capture/inference implementation remains TODO, so do not expect a working real-time command yet.
6. Before merging A/B/C work, run the [integration smoke test](docs/validation_plan.md).

## Role and Integration

| Role | Ownership | Deliverable / boundary |
| --- | --- | --- |
| A | Baseline and model | Versioned experiment config, final `.pt` checkpoint, checksum, class mapping, metrics |
| B | Streaming and inference | OpenCV video/frame capture, YOLO inference, bounding boxes, confidence, FPS/latency |
| C | Environment and validation | Reproducible setup, dataset preprocessing/validation, smoke tests, result verification |

Role A hands Role B a checkpoint plus its SHA-256 and `0=fire` class contract. Role B must not hard-code a developer-specific checkpoint path; the path must enter through project configuration or CLI. Role C verifies the environment, artifact checksum, missing-path behavior, and end-to-end smoke test. The current repository contains A's completed EXP-001 automation; B's real-time implementation and the combined integration test remain TODO.

## Model Handoff Contract

| Field | Contract |
| --- | --- |
| Weight format | Ultralytics `.pt` checkpoint |
| Validated artifact | EXP-001 `best.pt`, checksum shown above |
| Class mapping | Exactly `0=fire` for the baseline |
| Inference input | OpenCV BGR frame or supported image input |
| Detection output | Bounding-box coordinates, confidence, and class ID/name |
| Path injection | Config or CLI; never a machine-specific hard-coded path |
| Git policy | Do not commit `.pt` files or other large model artifacts |
| Failure behavior | Missing/unreadable weight path or wrong class mapping must fail fast |

Changing the class set, weight format, or output schema requires a new experiment and an explicit integration-contract update. Detailed real-time expectations are in the [real-time guide](docs/realtime_guide.md).

## Experiment Protocol

EXP-001 remains the immutable comparison baseline. A follow-up experiment must declare its hypothesis and change one major variable at a time while holding the remaining baseline settings fixed. Record configuration, dataset provenance, checkpoint checksum, metrics, and decision under `experiments/`.

The following are candidates only; none have been run:

| Candidate | Single primary change |
| --- | --- |
| EXP-002 | Add hard-negative examples |
| EXP-003 | Add one additional fire dataset |
| EXP-004 | Change from `fire` to `fire/smoke` multi-class detection |
| EXP-005 | Tune image size or augmentation in separately scoped trials |
| EXP-006 | Tune real-time confidence/NMS thresholds without retraining the baseline |

See the [training guide](docs/training_guide.md) and [experiment template](experiments/README.md).

## Integration Smoke Test

After A/B/C code is combined, verify at minimum:

- validated `best.pt` loads;
- sample-image inference returns a fire detection result or a valid empty result;
- video/frame inference processes consecutive OpenCV frames;
- bounding boxes render at valid frame coordinates;
- confidence values render with detections;
- FPS or per-frame latency is reported;
- class ID `0` is rendered as `fire`;
- a missing weight path fails before capture/inference starts.

Detailed evidence and acceptance criteria belong in the [validation plan](docs/validation_plan.md). No end-to-end real-time smoke test has passed yet because the B pipeline is not implemented.

## Distribution Rules

- Never commit API keys, tokens, `.env` secrets, or credentials in notebooks/configs.
- Never commit the raw Roboflow export or other large source datasets.
- Never commit `*.pt` checkpoints; distribute them separately with a SHA-256 checksum.
- Preserve dataset, model, repository, commit, and license provenance.
- Participant workflow should be clone -> setup -> configure artifact/source -> run; retraining is an explicit experiment action.
- Do not describe external upstream source as project-owned code or remove its attribution/license boundary.

See [data handling](docs/data_guide.md), [open-source references](docs/open_source_references.md), and [external-source policy](external/README.md).

## Current Status

| Area | Status |
| --- | --- |
| EXP-001 baseline reproduction | Completed and verified |
| Colab setup/verifier | Completed and verified |
| Dataset preparation/validation | Completed for EXP-001 |
| Final checkpoint handoff metadata | Completed; binary distributed outside Git |
| OpenCV real-time inference | TODO |
| Smartphone/drone streaming method | TODO |
| A/B/C integration smoke test | TODO |
| Follow-up experiments | Candidates only; not run |
