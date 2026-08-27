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

Precision: approximately `0.993`
Recall: approximately `0.979`
mAP50: approximately `0.989`
mAP50-95: approximately `0.628`

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

### Attempt 2

- Python 3.10.21 PASS
- torch 2.0.1+cu118 PASS
- torchvision 0.15.2+cu118 PASS
- CUDA 11.8 PASS
- NumPy 1.26.4 PASS
- Tesla T4 PASS
- Ultralytics 8.0.20 PASS
- Roboflow FAIL: missing dotenv
- Training not run

Roboflow `1.4.1` and python-dotenv `1.2.3` are project-side reproduction dependencies. Their versions were not specified by the upstream notebook.

### Attempt 3

- Dependency resolution failed before environment verification.
- The PyTorch CUDA 11.8 index was also used for general dependencies and exposed only `idna==3.4` to uv.
- Roboflow `1.4.1` requires `idna>=3.7`; requests `2.28.1` permits `idna>=2.5,<4`, so the packages have a compatible intersection.
- This was an index-scoping failure, not a Roboflow/Ultralytics incompatibility.
- Training was not run.

### Attempt 4

- Dependency resolution failed during the torch/torchvision installation step.
- Torchvision's general dependencies, including requests and idna, were incorrectly resolved against the PyTorch CUDA 11.8 index.
- The failure did not invalidate `idna==3.10`; it exposed that the CUDA index still had transitive dependency scope.
- Training was not run.

## Dataset Preparation and Validation

Before training, run the launcher with `--prepare-only`. This downloads only Roboflow dataset version 1, validates `data.yaml`, split paths, class 0 (`fire`), image/label presence, and every YOLO label's five fields and normalized coordinates. It prints split counts and the dataset location, then exits without loading a YOLO model, training, or validation inference.

The first dataset preparation run downloaded the expected split directories but failed because the exported `data.yaml` contained `../train/images`, `../valid/images`, and `../test/images`, which resolved outside the returned dataset root. The launcher now preserves that original file and creates `data.exp001-normalized.yaml` with verified absolute split paths. Both preparation validation and full training use the normalized file.

## Actual Training Run

- All 50 epochs completed successfully in Colab.
- `runs/detect/train2/weights/best.pt` and `last.pt` were created.
- Final best.pt validation completed with the metrics recorded above.
- Post-processing then failed because Ultralytics `8.0.20` returns `None` from `model.train()`, while the launcher expected `results.save_dir`.
- Plotting threads also reported `FreeTypeFont.getsize` errors caused by a newer Pillow release; the EXP-001 environment now pins Pillow `9.5.0` without changing Ultralytics.
