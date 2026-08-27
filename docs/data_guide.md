# Data Guide

## EXP-001 Dataset

The verified baseline uses the FLAME-derived Roboflow project `tim-4ijf0/drone-fire-detection-byija`, version 1.

| Split | Images |
| --- | ---: |
| train | 106 |
| val | 31 |
| test | 15 |

Class mapping is exactly `0=fire`. EXP-001 preparation validates image/label presence, five-field YOLO labels, normalized coordinates in `[0,1]`, and split paths. Because the exported YAML paths did not match the returned directory layout, project automation creates a separate `data.exp001-normalized.yaml`; it does not edit the Roboflow source YAML.

See [EXP-001-baseline.md](../experiments/EXP-001-baseline.md) for the authoritative result and [colab_baseline_guide.md](colab_baseline_guide.md) for controlled preparation.

## Storage Rules

- Do not commit raw dataset exports, generated splits, labels, caches, or credentials.
- Keep test data separate from training and tuning.
- Record provider, project/version, class mapping, split counts, and license/provenance.
- Put local data only under ignored `data/` locations or the runtime-specific download directory.
- Do not treat an external dataset as project-owned data.

## Follow-up Data Work

Hard negatives, additional fire data, and fire/smoke relabeling are separate candidate experiments. Each requires a new experiment ID, provenance record, split audit, and class-contract review. These candidates have not been executed.
