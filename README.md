# Real-time Fire Detection

## Project Introduction

This project aims to receive video from a smartphone or drone camera on a laptop and detect Fire / Smoke with a YOLO-based model. The smartphone or drone is responsible for capture and transmission; YOLO inference runs on the laptop.

## Goal

The target pipeline is:

```text
Video input -> real-time inference -> Fire / Smoke bounding boxes
             -> confidence -> FPS / latency measurement
```

## Overall Pipeline

```text
Smartphone / Drone Camera
        -> Streaming
        -> Laptop
        -> OpenCV
        -> YOLO
        -> Fire / Smoke Detection
        -> Bounding Box / Confidence
        -> FPS / Latency
```

## Quick Start

**Status: Not implemented yet**

Planned flow:

1. Clone or download the repository.
2. Install the verified environment.
3. Prepare the model.
4. Configure the video source.
5. Run real-time detection.

TODO: Add verified commands after the pipeline and environment are validated.

## Repository Structure

| Directory | Purpose |
| --- | --- |
| `configs/` | Data, model, and inference settings |
| `data/` | Raw, intermediate, processed, negative, and split data |
| `models/` | Pretrained and project checkpoint locations |
| `src/` | Internal source code organized by function |
| `scripts/` | User-facing entry-point locations |
| `experiments/` | Experiment records and metadata |
| `external/` | External source and license records |
| `docs/` | Setup, operation, validation, and attribution guides |
| `tests/` | Future preprocessing and inference tests |
| `assets/` | Small documentation and demo assets |

## Data

Large datasets are not committed to Git. See [`data/README.md`](data/README.md) and [`docs/data_guide.md`](docs/data_guide.md) for the planned data workflow.

## Model

Large model weights are not committed to Git. See [`models/README.md`](models/README.md) for the expected locations and TODOs.

## Realtime Detection

The intended deployment flow is smartphone or drone video transmission to a laptop, followed by OpenCV capture and YOLO inference on the laptop. The streaming method and application are not fixed yet. See [`docs/realtime_guide.md`](docs/realtime_guide.md).

## Validation

Validation will cover dataset metrics, controlled video validation, and real-time pipeline behavior. See [`docs/validation_plan.md`](docs/validation_plan.md).

## Documentation

Start with [`docs/environment_setup.md`](docs/environment_setup.md), then consult the data, training, real-time, and validation guides as those parts are implemented.

## Open-source / Dataset Attribution

External repositories, datasets, papers, licenses, versions, and changes will be recorded in [`docs/open_source_references.md`](docs/open_source_references.md) and [`external/README.md`](external/README.md). No source has been selected or cloned yet.

## Current Status

```text
Repository structure: Ready
Dataset pipeline: TODO
Baseline model: TODO
Training pipeline: TODO
Realtime streaming: TODO
Validation: TODO
Distribution guide: TODO
```