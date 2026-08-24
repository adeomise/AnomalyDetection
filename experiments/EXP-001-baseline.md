# EXP-001 - Baseline Reproduction

## Objective

Reproduce the selected external aerial Fire Detection baseline repository under its original conditions before applying project-specific modifications.

## Source

Repository: `https://github.com/tim3in/Fire-Detection-Drone.git`
Commit / Tag: `e90632a25a07ea1f2137681741e3d9bfc8f1cb3c` / No tag found

## Dataset

Dataset: FLAME-derived Roboflow project `tim-4ijf0/drone-fire-detection-byija`, version 1
Classes: `0: fire` (verify against generated `data.yaml`)
Split: Roboflow-generated train/valid/test split; exact structure and counts TODO

## Model

Model: Ultralytics YOLOv8 medium (`yolov8m.pt`)
Pretrained weight: `yolov8m.pt`; output `runs/detect/train/weights/best.pt`

## Training Configuration

Image size: `800`
Epochs: `50`
Batch size: TODO
Optimizer: TODO
Learning rate: TODO

## Changes from Original

None.

## Results

Precision: TODO
Recall: TODO
mAP50: TODO
mAP50-95: TODO

## Reproduction Status

Not ready - environment, exported dataset structure, license, and reproducible dependency details remain incomplete.

## Notes

TODO: Obtain and verify the Roboflow export, environment details, and license status before running EXP-001. See `docs/baseline_analysis.md` for source findings. Upstream source remains read-only during this experiment.