#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="browser-bot.service"
TIMER_NAME="browser-bot.timer"

# The directory where systemd user units should be placed
SYSTEMD_USER_DIR="${HOME}/.config/systemd/user"

# Get the directory of this script to locate the systemd files relative to it
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing systemd user units..."

# Ensure the systemd user directory exists
mkdir -p "$SYSTEMD_USER_DIR"

# Copy the unit files
echo "Copying unit files to $SYSTEMD_USER_DIR..."
cp "$SCRIPT_DIR/systemd/$SERVICE_NAME" "$SYSTEMD_USER_DIR/"
cp "$SCRIPT_DIR/systemd/$TIMER_NAME" "$SYSTEMD_USER_DIR/"

# Reload systemd user daemon so it recognizes the new files
echo "Reloading systemd user daemon..."
systemctl --user daemon-reload

# Enable and start the timer
echo "Enabling and starting the timer..."
systemctl --user enable --now "$TIMER_NAME"

echo "Installation complete."