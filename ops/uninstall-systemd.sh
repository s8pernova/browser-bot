#!/usr/bin/env bash
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root. Please use sudo."
   exit 1
fi

if [[ $# -ne 1 ]]; then
    echo "Usage: sudo $0 <service-prefix-name>"
    echo "Example: sudo $0 brianna-voting-browser-bot"
    exit 1
fi

SERVICE_PREFIX="$1"
SERVICE_NAME="${SERVICE_PREFIX}.service"
TIMER_NAME="${SERVICE_PREFIX}.timer"

SYSTEMD_DIR="/etc/systemd/system"

echo "Uninstalling system-wide units for $SERVICE_PREFIX..."

# Stop and disable the timer
echo "Stopping and disabling timer..."
# Use `|| true` so the script doesn't crash if it's already stopped/disabled
systemctl disable --now "$TIMER_NAME" || true

# Also stop the service in case it's currently running
echo "Stopping service if running..."
systemctl stop "$SERVICE_NAME" || true

# Reset failed state in case the service crashed previously
echo "Resetting failed state..."
systemctl reset-failed "$SERVICE_NAME" || true
systemctl reset-failed "$TIMER_NAME" || true

# Remove the unit files
echo "Removing unit files from $SYSTEMD_DIR..."
rm -f "$SYSTEMD_DIR/$SERVICE_NAME"
rm -f "$SYSTEMD_DIR/$TIMER_NAME"

# Reload systemd user daemon
echo "Reloading systemd daemon..."
systemctl daemon-reload

echo "Uninstallation complete."