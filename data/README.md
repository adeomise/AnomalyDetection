# Data

Datasets are kept outside Git. Store local or downloaded data under the appropriate directory and record its source, version, and processing history in the documentation.

| Directory | Role |
| --- | --- |
| `raw/` | Original downloads, preserved without direct modification |
| `interim/` | Temporary conversion, cleaning, and preprocessing results |
| `processed/` | Data prepared for YOLO training |
| `negatives/` | Fire-like hard-negative images; optional empty YOLO labels may be associated with them |
| `splits/` | Train, validation, and test split definitions |

Place data in the directory matching its processing stage. Keep the test set separate from training and tuning workflows. See [`docs/data_guide.md`](../docs/data_guide.md) for the future detailed workflow.

TODO: Select datasets, define the exact directory layout, and document the verified preparation process.