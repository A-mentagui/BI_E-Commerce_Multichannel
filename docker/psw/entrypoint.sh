#!/usr/bin/env bash
set -euo pipefail

PSW_HOME="${PSW_HOME:-/opt/psw/workbench-schema}"
WORKSPACE_DIR="${WORKSPACE_DIR:-/workspace}"

# Execute the command passed as arguments
if [[ $# -eq 0 ]]; then
  # Default to bash shell if no arguments provided
  exec bash
else
  # Execute the provided command
  exec "$@"
fi
