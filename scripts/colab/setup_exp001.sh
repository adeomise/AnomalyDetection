#!/usr/bin/env bash
set -euo pipefail

ENV_DIR="${BASELINE_ENV_DIR:-/content/baseline-env}"
PYTHON_VERSION="3.10"

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

echo "Provisioning Python ${PYTHON_VERSION} in ${ENV_DIR}..."
uv python install "${PYTHON_VERSION}"
uv venv --python "${PYTHON_VERSION}" "${ENV_DIR}"

PYTHON="${ENV_DIR}/bin/python"
[[ -x "${PYTHON}" ]] || { echo "ERROR: baseline Python was not created." >&2; exit 1; }

echo "Installing the pinned baseline training stack..."
uv pip install --python "${PYTHON}" \
  --index-url https://download.pytorch.org/whl/cu118 \
  "torch==2.0.1"
uv pip install --python "${PYTHON}" "ultralytics==8.0.20" "roboflow"

echo "Installed versions:"
"${PYTHON}" -c 'import sys, torch, ultralytics; print("Python:", sys.version); print("PyTorch:", torch.__version__); print("Torch CUDA:", torch.version.cuda); print("Ultralytics:", ultralytics.__version__)'

"${PYTHON}" "$(dirname "$0")/verify_exp001.py"
echo "Environment setup: PASS"