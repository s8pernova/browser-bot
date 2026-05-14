#!/usr/bin/env bash
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root. Use sudo."
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

systemctl disable --now "$TIMER_NAME" || true
systemctl stop "$SERVICE_NAME" || true

systemctl reset-failed "$SERVICE_NAME" || true
systemctl reset-failed "$TIMER_NAME" || true

rm -f "$SYSTEMD_DIR/$SERVICE_NAME"
rm -f "$SYSTEMD_DIR/$TIMER_NAME"

systemctl daemon-reload

echo "Uninstallation complete."