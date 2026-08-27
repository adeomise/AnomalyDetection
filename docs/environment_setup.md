# Environment Setup

## Verified EXP-001 Environment

EXP-001 setup and verification passed in a clean Google Colab GPU runtime.

| Component | Verified value |
| --- | --- |
| Python | 3.10.21 |
| PyTorch | 2.0.1+cu118 |
| Torchvision | 0.15.2+cu118 |
| PyTorch CUDA build | 11.8 |
| NumPy | 1.26.4 |
| Ultralytics | 8.0.20 |
| Roboflow | 1.4.1 |
| python-dotenv | 1.2.3 |
| Pillow | 9.5.0 |
| Verified GPU | Tesla T4 |

The constraints are in [exp001-constraints.txt](../configs/environment/exp001-constraints.txt). The setup isolates Python under `/content/baseline-env`, scopes the PyTorch CUDA index to torch/torchvision wheels, resolves general dependencies from PyPI, runs `uv pip check`, and then runs the strict verifier.

## Colab Setup

From the repository root in a Colab GPU runtime:

```bash
bash scripts/colab/setup_exp001.sh
```

Continue only after both of these appear:

```text
environment verification: PASS
Environment setup: PASS
```

The verifier checks exact Python major/minor, torch, torchvision, CUDA build, NumPy, Ultralytics, Roboflow, python-dotenv, `pkg_resources`, CUDA availability, and GPU detection. See [colab_baseline_guide.md](colab_baseline_guide.md) for secrets and supported workflow modes.

## Boundaries

- Do not install the EXP-001 stack into Windows global Python.
- Do not replace pinned torch or Ultralytics with a newer release.
- Do not expose `ROBOFLOW_API_KEY` in notebooks, commands, logs, or files.
- Do not assume a Colab setup is the production laptop environment.
- Do not require full baseline retraining for participant onboarding.

Role C owns future laptop environment packaging and reproducibility tests. A supported laptop setup command remains TODO.

## Historical Resolution Notes

Initial attempts exposed torch resolver upgrades, removed `pkg_resources`, missing `dotenv`, incorrectly scoped package indexes, Roboflow YAML paths, Ultralytics 8.0.20 return-value behavior, and Pillow compatibility. The complete attempt history and final resolution are retained in [EXP-001-baseline.md](../experiments/EXP-001-baseline.md).
