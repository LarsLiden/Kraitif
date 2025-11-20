#!/usr/bin/env bash

set -euo pipefail

GREEN="$(printf '\033[0;32m')"
YELLOW="$(printf '\033[1;33m')"
RED="$(printf '\033[0;31m')"
BLUE="$(printf '\033[0;34m')"
NC="$(printf '\033[0m')"

info() {
  echo -e "${GREEN}$1${NC}"
}

warn() {
  echo -e "${YELLOW}$1${NC}"
}

error() {
  echo -e "${RED}$1${NC}" >&2
}

usage() {
  cat <<'EOF'
Usage: ./start.sh [options]

Options:
  -q, --quickstart   Skip dependency installation and assume the environment is ready.
  -h, --help         Show this help message and exit.
EOF
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_DIR=".venv"

QUICKSTART=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    -q|--quickstart)
      QUICKSTART=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      error "Unknown option: $1"
      usage
      exit 1
      ;;
  esac
done

choose_python() {
  if [[ -n "${PYTHON_BIN:-}" ]]; then
    echo "$PYTHON_BIN"
    return
  fi
  if command -v python3 >/dev/null 2>&1; then
    echo "python3"
  elif command -v python >/dev/null 2>&1; then
    echo "python"
  else
    error "Neither python3 nor python was found on PATH."
    exit 1
  fi
}

PYTHON_CMD="$(choose_python)"

info "Starting Kraitif Story Generator..."

if [[ "$QUICKSTART" -eq 1 ]]; then
  info "Quickstart mode enabled; skipping dependency installation."
fi

if [[ ! -d "$VENV_DIR" ]]; then
  if [[ "$QUICKSTART" -eq 1 ]]; then
    error "Virtual environment not found at ${VENV_DIR}. Run without --quickstart first."
    exit 1
  fi
  warn "Python virtual environment not found at ${VENV_DIR}. Creating..."
  "$PYTHON_CMD" -m venv "$VENV_DIR"
fi

if [[ -f "${VENV_DIR}/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source "${VENV_DIR}/bin/activate"
elif [[ -f "${VENV_DIR}/Scripts/activate" ]]; then
  # shellcheck disable=SC1091
  source "${VENV_DIR}/Scripts/activate"
else
  error "Unable to locate activation script for ${VENV_DIR}."
  exit 1
fi

if [[ "$QUICKSTART" -eq 0 ]]; then
  info "Installing Python dependencies..."
  pip install --upgrade pip
  pip install -r requirements.txt

  "$PYTHON_CMD" <<'PYCODE'
import importlib
missing = []
for module in ("flask", "openai"):
  try:
    importlib.import_module(module)
  except ModuleNotFoundError:
    missing.append(module)

if missing:
  mods = ", ".join(missing)
  raise SystemExit(f"Missing required modules: {mods}. Check requirements.txt installation.")
PYCODE
else
  warn "Skipping dependency installation; ensure requirements are already satisfied."
fi

export FLASK_APP="${FLASK_APP:-app}"
export FLASK_ENV="${FLASK_ENV:-development}"
export FLASK_RUN_PORT="${FLASK_RUN_PORT:-8005}"
export FLASK_DEBUG="${FLASK_DEBUG:-1}"
export PYTHONPATH="${PYTHONPATH:-$SCRIPT_DIR}"

info "Configuration:"
echo -e "  ${BLUE}Python:${NC} $(command -v python)"
echo -e "  ${BLUE}Virtual env:${NC} $VENV_DIR"
echo -e "  ${BLUE}FLASK_APP:${NC} $FLASK_APP"
echo -e "  ${BLUE}FLASK_ENV:${NC} $FLASK_ENV"
echo -e "  ${BLUE}FLASK_RUN_PORT:${NC} $FLASK_RUN_PORT"
echo -e "  ${BLUE}FLASK_DEBUG:${NC} $FLASK_DEBUG"

info "Starting Flask server..."
info "Open your browser to http://localhost:${FLASK_RUN_PORT}"
echo ""

DEBUG_FLAG="${FLASK_DEBUG,,}"
if [[ "$DEBUG_FLAG" == "0" || "$DEBUG_FLAG" == "false" ]]; then
  exec "$PYTHON_CMD" -m flask run --port "$FLASK_RUN_PORT"
else
  exec "$PYTHON_CMD" -m flask run --debug --port "$FLASK_RUN_PORT"
fi
