#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <service-prefix-name> <workflow-file.yaml>"
    echo "Example: $0 brianna-voting-browser-bot workflows/vote_for_brianna.yaml"
    exit 1
fi

SERVICE_PREFIX="$1"
WORKFLOW_FILE="$2"

SERVICE_NAME="${SERVICE_PREFIX}.service"
TIMER_NAME="${SERVICE_PREFIX}.timer"

# The directory where systemd user units should be placed
SYSTEMD_USER_DIR="${HOME}/.config/systemd/user"

# Get the directory of this script to locate the systemd files relative to it
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing systemd user units for $SERVICE_PREFIX..."

# Ensure the systemd user directory exists
mkdir -p "$SYSTEMD_USER_DIR"

# Copy and template the unit files
echo "Generating unit files to $SYSTEMD_USER_DIR..."
sed "s|{{WORKFLOW_FILE}}|$WORKFLOW_FILE|g" "$SCRIPT_DIR/systemd/browser-bot.service.template" > "$SYSTEMD_USER_DIR/$SERVICE_NAME"

# The timer doesn't need templating currently, so we just copy it
cp "$SCRIPT_DIR/systemd/browser-bot.timer.template" "$SYSTEMD_USER_DIR/$TIMER_NAME"

# Reload systemd user daemon so it recognizes the new files
echo "Reloading systemd user daemon..."
systemctl --user daemon-reload

# Enable and start the timer
echo "Enabling and starting the timer..."
systemctl --user enable --now "$TIMER_NAME"

echo "Installation complete."
echo ""
echo "Useful commands:"
echo "  Check timer status:   systemctl --user status $TIMER_NAME"
echo "  Check service status: systemctl --user status $SERVICE_NAME"
echo "  View execution logs:  journalctl --user -u $SERVICE_NAME -f"