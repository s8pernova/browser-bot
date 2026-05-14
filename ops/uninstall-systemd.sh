#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="browser-bot.service"
TIMER_NAME="browser-bot.timer"
SYSTEMD_USER_DIR="${HOME}/.config/systemd/user"

echo "Uninstalling systemd user units..."

# Stop and disable the timer
echo "Stopping and disabling timer..."
# Use `|| true` so the script doesn't crash if it's already stopped/disabled
systemctl --user disable --now "$TIMER_NAME" || true

# Also stop the service in case it's currently running
systemctl --user stop "$SERVICE_NAME" || true

# Remove the unit files
echo "Removing unit files from $SYSTEMD_USER_DIR..."
rm -f "$SYSTEMD_USER_DIR/$SERVICE_NAME"
rm -f "$SYSTEMD_USER_DIR/$TIMER_NAME"

# Reload systemd user daemon
echo "Reloading systemd user daemon..."
systemctl --user daemon-reload

# Reset failed state in case the service crashed previously
systemctl --user reset-failed "$SERVICE_NAME" || true

echo "Uninstallation complete."