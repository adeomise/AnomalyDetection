# Baseline Analysis

This document records facts needed to reproduce a candidate upstream Fire Detection repository. It must be based on the upstream README, notebooks, scripts, configuration, requirements, and a specific commit or tag. Unverified values remain `TODO` or `Not specified`.

## 1. Repository Information

Repository: TODO — identify baseline repository
URL: TODO — verify URL
Commit / Tag: TODO — record exact revision
License: TODO — verify license

## 2. Model

YOLO version: TODO — verify
Framework: TODO — verify
Pretrained weight: TODO — verify
Input image size: TODO — verify

## 3. Dataset

Dataset name: TODO — verify
Dataset source: TODO — verify source and access method
Dataset type: TODO — verify
Classes: TODO — verify names and count
Label format: TODO — verify

## 4. Dataset Structure

Not specified until the upstream source is identified and inspected.

```text
TODO — record the exact upstream directory structure; do not normalize it by assumption.
```

Required items to verify:

- Dataset root
- Train images and labels
- Validation images and labels
- Test images and labels
- `data.yaml` location
- Class names and number of classes

## 5. Training Configuration

Epochs: TODO — verify
Batch size: TODO — verify
Image size: TODO — verify
Optimizer: TODO — verify
Learning rate: TODO — verify
Augmentation: TODO — verify

## 6. Training Procedure

TODO — summarize the original README, notebook, or script execution order after inspection. Do not add a command until it has been confirmed in the upstream source.

Training configuration sources:

- README section: TODO
- Notebook: TODO
- Script/config: TODO
- Commit: TODO

## 7. Inference Procedure

TODO — summarize the inference method provided by the upstream source. Do not invent a command or input format.

## 8. Outputs

Weights: TODO — verify
Metrics: TODO — verify
Result directory: TODO — verify

## 9. Reported Performance

Precision: TODO — verify
Recall: TODO — verify
mAP50: TODO — verify
mAP50-95: TODO — verify

Only values explicitly reported by the upstream source may be entered here.

## 10. Known Limitations

TODO — record only limitations stated in the upstream README or source. Do not infer limitations from the repository name alone.

## 11. Reproduction Requirements

- Identified upstream repository URL
- Pinned upstream commit or tag
- Verified license and attribution requirements
- Verified Python, framework, and dependency requirements
- Verified dataset source and exact directory structure
- Verified class definitions and label format
- Verified pretrained weight source and expected location
- Verified original training configuration and command
- A separate reproduction record in `experiments/EXP-001-baseline.md`

## 12. Open Questions

- TODO — Which upstream repository is the selected baseline?
- TODO — Which commit or tag will be reproduced?
- TODO — Is the license compatible with the planned project distribution?
- TODO — What are the exact environment, dataset, model, and training requirements?
- TODO — Has the original baseline been reproduced without project-specific changes?

## Source Boundary

The upstream repository is read-only during baseline analysis and original-condition reproduction. Once reproduction is complete, integration changes may be considered only after verifying that the license permits modification and redistribution. Prefer a project-local wrapper, adapter, or independent implementation; if upstream files are modified, record the license, source revision, modified files, and changes in the provenance documents.