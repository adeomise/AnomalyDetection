#!/usr/bin/env bash
set -euo pipefail

ENV_DIR="${BASELINE_ENV_DIR:-/content/baseline-env}"
PYTHON_VERSION="3.10"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
CONSTRAINTS="${PROJECT_ROOT}/configs/environment/exp001-constraints.txt"
PYTORCH_INDEX="https://download.pytorch.org/whl/cu118"

if [[ "$(uname -s)" != "Linux" ]]; then
  echo "ERROR: setup_exp001.sh must run in a Linux/Colab runtime." >&2
  exit 1
fi

if ! command -v uv >/dev/null 2>&1; then
  echo "Installing uv for this Colab runtime..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="${HOME}/.local/bin:${PATH}"
fi

command -v uv >/dev/null 2>&1 || { echo "ERROR: uv is unavailable after installation." >&2; exit 1; }
[[ -f "${CONSTRAINTS}" ]] || { echo "ERROR: EXP-001 constraints not found: ${CONSTRAINTS}" >&2; exit 1; }

echo "Provisioning Python ${PYTHON_VERSION} in ${ENV_DIR}..."
uv python install "${PYTHON_VERSION}"
uv venv --python "${PYTHON_VERSION}" "${ENV_DIR}"

PYTHON="${ENV_DIR}/bin/python"
[[ -x "${PYTHON}" ]] || { echo "ERROR: baseline Python was not created." >&2; exit 1; }

echo "Installing the pinned baseline training stack..."
uv pip install --python "${PYTHON}" \
  --constraint "${CONSTRAINTS}" \
  "setuptools>=65,<82" "numpy==1.26.4"
uv pip install --python "${PYTHON}" \
  --constraint "${CONSTRAINTS}" \
  --index-url "${PYTORCH_INDEX}" \
  "torch==2.0.1+cu118" "torchvision==0.15.2+cu118"

# Resolve general dependencies from PyPI under the core-stack constraints.
# The CUDA index is intentionally scoped to the torch/torchvision step above.
uv pip install --python "${PYTHON}" \
  --constraint "${CONSTRAINTS}" \
  "ultralytics==8.0.20" "roboflow==1.4.1" "python-dotenv==1.2.3"

uv pip check --python "${PYTHON}"

echo "Installed versions:"
"${PYTHON}" -c 'import sys, torch, torchvision, ultralytics; from importlib.metadata import version; print("Python:", sys.version); print("PyTorch:", torch.__version__); print("Torchvision:", torchvision.__version__); print("Torch CUDA:", torch.version.cuda); print("Ultralytics:", ultralytics.__version__); print("Roboflow:", version("roboflow")); print("python-dotenv:", version("python-dotenv"))'

"${PYTHON}" "${SCRIPT_DIR}/verify_exp001.py"
echo "Environment setup: PASS"
