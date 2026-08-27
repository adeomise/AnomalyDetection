# Realtime Guide

## Status

The laptop-side OpenCV streaming and real-time inference pipeline is not implemented yet. This document defines the interface Role B must implement against Role A's completed EXP-001 model handoff.

## Target Flow

```text
Smartphone / drone stream
  -> OpenCV frame on laptop
  -> YOLO checkpoint inference
  -> bbox + confidence + class
  -> rendered frame + FPS / latency
```

The capture application, stream protocol/URL, reconnect behavior, and supported operating system are still TODO.

## Model Handoff Contract

| Field | Requirement |
| --- | --- |
| Weight | Ultralytics `.pt` checkpoint supplied outside Git |
| Baseline class | Exactly `0=fire` |
| Input | OpenCV BGR frame or a supported image path/array |
| Output | Bounding-box coordinates, confidence, and class ID/name |
| Configuration | Model path and thresholds supplied by config or CLI |
| Failure | Missing/unreadable weight must fail before opening the stream |
| Provenance | Experiment ID and checkpoint SHA-256 retained in run output/logs |

Validated EXP-001 checkpoint SHA-256:

```text
7b1fe847ea81bf5cd3647da1d457510b4a87d956be9eed4ab61c92db817f5ef2
```

Role B must not rename class 0, silently substitute another model, or commit the checkpoint. A multi-class output is a different experiment and contract.

## Role B Implementation Requirements

- accept model and video source through project-side configuration or CLI;
- load the model once, outside the frame loop;
- preserve OpenCV frame dimensions and clamp rendered coordinates;
- render class name and confidence for each detection;
- report measured FPS or per-frame latency;
- handle end-of-stream and capture failure explicitly;
- avoid logging secrets embedded in stream URLs;
- expose a deterministic image mode for smoke testing.

## Integration Boundary

Role A provides checkpoint, checksum, class mapping, and metrics. Role B owns capture, inference adaptation, rendering, and performance reporting. Role C verifies environment compatibility, artifact identity, fail-fast behavior, and smoke-test evidence.

There is currently no supported real-time command. Add one under `scripts/realtime/` only when its implementation and minimum smoke tests exist.
