#!/bin/bash
# VENOM Λ-GENESIS Systemd Services Uninstallation Script
# Stops, disables, and removes all VENOM Lambda services

set -e  # Exit on error

echo "🧬 VENOM Λ-GENESIS Service Uninstallation"
echo "=========================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Error: This script must be run as root (use sudo)"
    exit 1
fi

# List of services to uninstall
SERVICES=(
    "venom-fractal.service"
    "venom-api.service"
    "venom-mesh-discovery.service"
    "venom-mesh-orchestrator.service"
)

echo ""
echo "🛑 Stopping and disabling services..."
echo ""

# Stop and disable each service
for SERVICE in "${SERVICES[@]}"; do
    SERVICE_PATH="/etc/systemd/system/$SERVICE"
    
    if [ -f "$SERVICE_PATH" ]; then
        echo "🛑 Stopping $SERVICE..."
        
        # Stop the service
        if systemctl is-active --quiet "$SERVICE"; then
            systemctl stop "$SERVICE" 2>&1 | sed 's/^/    /'
            echo "✅ $SERVICE stopped"
        else
            echo "⚪ $SERVICE was not running"
        fi
        
        # Disable the service
        if systemctl is-enabled --quiet "$SERVICE" 2>/dev/null; then
            systemctl disable "$SERVICE" 2>&1 | sed 's/^/    /'
            echo "✅ $SERVICE disabled"
        else
            echo "⚪ $SERVICE was not enabled"
        fi
        
        echo ""
    else
        echo "⚪ $SERVICE not found, skipping..."
        echo ""
    fi
done

echo "🗑️  Removing service files..."
echo ""

# Remove service files
for SERVICE in "${SERVICES[@]}"; do
    SERVICE_PATH="/etc/systemd/system/$SERVICE"
    
    if [ -f "$SERVICE_PATH" ]; then
        echo "🗑️  Removing $SERVICE..."
        rm -f "$SERVICE_PATH"
        echo "✅ $SERVICE removed"
    fi
done

echo ""
echo "🔄 Reloading systemd daemon..."
systemctl daemon-reload
systemctl reset-failed 2>/dev/null || true

echo ""
echo "📊 Verifying removal..."
REMAINING=$(systemctl list-units --type=service --all | grep venom | wc -l)

if [ "$REMAINING" -eq 0 ]; then
    echo "✅ All VENOM services successfully removed"
else
    echo "⚠️  Some VENOM services may still be present:"
    systemctl list-units --type=service --all | grep venom || true
fi

echo ""
echo "✅ Uninstallation Complete!"
echo ""
echo "📝 Note: Service logs are still available in journalctl"
echo "   To view old logs: journalctl -u venom-api.service"
echo ""
echo "🔧 To reinstall, run: sudo ./install-services.sh"
