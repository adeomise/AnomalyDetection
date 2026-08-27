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
Batch size: `16` (resolved upstream training output)
Optimizer: TODO - not specified by upstream command
Learning rate: TODO - not specified by upstream command

## Changes from Original

None.

## Results

Precision: TODO
Recall: TODO
mAP50: TODO
mAP50-95: TODO

## Reproduction Status

Not ready - local environment, exported dataset structure, license, and reproducible dependency details remain incomplete.

## Environment Checklist

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

## Notes

TODO: Obtain and verify the Roboflow export, environment details, and license status before running EXP-001. See `docs/baseline_analysis.md` for source findings. Upstream source remains read-only during this experiment.

### Initial Colab automation test

- Python 3.10.21 provisioning succeeded.
- torch 2.0.1+cu118 was initially installed.
- Later dependency resolution upgraded torch to 2.13.0+cu130.
- ultralytics 8.0.20 import failed because pkg_resources was unavailable.
- Verification correctly returned FAIL.
- Training was not executed.
