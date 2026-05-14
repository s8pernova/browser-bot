#!/usr/bin/env bash
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root. Please use sudo."
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

# The directory where systemd user units should be placed
SYSTEMD_DIR="/etc/systemd/system"

# Get the directory of this script to locate the systemd files relative to it
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "Installing system-wide systemd units for $SERVICE_PREFIX as $EXEC_USER..."

# Copy and template the unit files
echo "Generating unit files to $SYSTEMD_DIR..."
sed "s|{{WORKFLOW_FILE}}|$WORKFLOW_FILE|g; s|{{PROJECT_ROOT}}|$PROJECT_ROOT|g; s|{{EXEC_USER}}|$EXEC_USER|g" \
  "$SCRIPT_DIR/systemd/browser-bot.service.template" > "$SYSTEMD_DIR/$SERVICE_NAME"

# The timer doesn't need templating currently, so we just copy it
cp "$SCRIPT_DIR/systemd/browser-bot.timer.template" "$SYSTEMD_DIR/$TIMER_NAME"

# Reload systemd user daemon so it recognizes the new files
echo "Reloading systemd daemon..."
systemctl daemon-reload

# Enable and start the timer
echo "Enabling and starting the timer..."
systemctl enable --now "$TIMER_NAME"

echo "Installation complete."