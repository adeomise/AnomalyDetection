# Open-source References

Record every external repository, dataset, paper, or library that materially informs or supplies this project.

## Baseline Repository

- Name: `tim3in/Fire-Detection-Drone`
- Type: GitHub Repository
- URL: https://github.com/tim3in/Fire-Detection-Drone.git
- Commit / Tag: `e90632a25a07ea1f2137681741e3d9bfc8f1cb3c` / No tag found
- License: TODO — verify license before any integration decision
- Purpose: Reproduce the upstream aerial fire detection baseline before project-specific changes
- YOLO version: YOLOv8
- Framework: Ultralytics
- Dataset: FLAME-derived Roboflow project `drone-fire-detection-byija`, version 1
- Classes: `0: fire`, confirmed by the EXP-001 dataset validation
- How it is used: Read-only reference during the completed baseline reproduction
- Changes made: None — original repository is used only as a read-only reference.
- Notes: EXP-001 reproduced the training notebook's `ultralytics==8.0.20`, `yolov8m.pt`, `epochs=50`, and `imgsz=800` baseline. No license file was found. Any integration modification requires a verified license permitting modification and redistribution. Prefer a wrapper, adapter, or independent implementation in this repository.

## Source Template

```text
Name:
Type:
URL:
Purpose:
License:
Version / Commit:
How it is used:
Files referenced:
Changes made:
Notes:
```

TODO: Populate this template only after each source and its license have been verified.
