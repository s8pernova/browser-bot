#!/usr/bin/env bash
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root. Use sudo."
    exit 1
fi

if [[ $# -ne 2 ]]; then
    echo "Usage: sudo $0 <service-prefix-name> <workflow-file.yaml>"
    echo "Example: sudo $0 brianna-voting-browser-bot workflows/vote-for-brianna.yaml"
    exit 1
fi

SERVICE_PREFIX="$1"
WORKFLOW_FILE="$2"

SERVICE_NAME="${SERVICE_PREFIX}.service"
TIMER_NAME="${SERVICE_PREFIX}.timer"

EXEC_USER="${EXEC_USER:-deploy}"
SYSTEMD_DIR="/etc/systemd/system"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

SERVICE_TEMPLATE="${SCRIPT_DIR}/systemd/browser-bot.service.template"
TIMER_TEMPLATE="${SCRIPT_DIR}/systemd/browser-bot.timer.template"

if [[ ! -f "$SERVICE_TEMPLATE" ]]; then
    echo "Missing service template: $SERVICE_TEMPLATE"
    exit 1
fi

if [[ ! -f "$TIMER_TEMPLATE" ]]; then
    echo "Missing timer template: $TIMER_TEMPLATE"
    exit 1
fi

if [[ ! -f "${PROJECT_ROOT}/${WORKFLOW_FILE}" ]]; then
    echo "Missing workflow file: ${PROJECT_ROOT}/${WORKFLOW_FILE}"
    exit 1
fi

if [[ ! -x "${PROJECT_ROOT}/.venv/bin/python" ]]; then
    echo "Missing executable venv Python: ${PROJECT_ROOT}/.venv/bin/python"
    exit 1
fi

echo "Installing system-wide systemd units for $SERVICE_PREFIX as $EXEC_USER..."
echo "Project root: $PROJECT_ROOT"

sed \
    -e "s|{{WORKFLOW_FILE}}|$WORKFLOW_FILE|g" \
    -e "s|{{PROJECT_ROOT}}|$PROJECT_ROOT|g" \
    -e "s|{{EXEC_USER}}|$EXEC_USER|g" \
    "$SERVICE_TEMPLATE" > "$SYSTEMD_DIR/$SERVICE_NAME"

cp "$TIMER_TEMPLATE" "$SYSTEMD_DIR/$TIMER_NAME"

systemctl daemon-reload
systemctl enable --now "$TIMER_NAME"

echo "Installation complete."