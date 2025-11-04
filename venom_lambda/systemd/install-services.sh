#!/bin/bash
# VENOM Λ-GENESIS Systemd Services Installation Script
# Installs and enables all VENOM Lambda services

set -e  # Exit on error

echo "🧬 VENOM Λ-GENESIS Service Installation"
echo "========================================"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Error: This script must be run as root (use sudo)"
    exit 1
fi

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENOM_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "📁 VENOM root directory: $VENOM_ROOT"

# Check if Python environment exists
if [ ! -f "$VENOM_ROOT/requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found in $VENOM_ROOT"
    exit 1
fi

# List of services to install
SERVICES=(
    "venom-fractal.service"
    "venom-api.service"
    "venom-mesh-discovery.service"
    "venom-mesh-orchestrator.service"
)

echo ""
echo "🔧 Installing systemd services..."
echo ""

# Install each service
for SERVICE in "${SERVICES[@]}"; do
    SERVICE_FILE="$SCRIPT_DIR/$SERVICE"
    
    if [ ! -f "$SERVICE_FILE" ]; then
        echo "⚠️  Warning: $SERVICE not found, skipping..."
        continue
    fi
    
    echo "📋 Installing $SERVICE..."
    
    # Copy service file to systemd directory
    cp "$SERVICE_FILE" /etc/systemd/system/
    
    # Replace placeholder paths in service file if needed
    sed -i "s|/path/to/venom|$VENOM_ROOT|g" "/etc/systemd/system/$SERVICE"
    
    echo "✅ $SERVICE installed"
done

echo ""
echo "🔄 Reloading systemd daemon..."
systemctl daemon-reload

echo ""
echo "🚀 Enabling and starting services..."
echo ""

# Enable and start each service
for SERVICE in "${SERVICES[@]}"; do
    SERVICE_NAME="${SERVICE}"
    
    if [ -f "/etc/systemd/system/$SERVICE_NAME" ]; then
        echo "▶️  Starting $SERVICE_NAME..."
        
        # Enable service to start on boot
        systemctl enable "$SERVICE_NAME" 2>&1 | sed 's/^/    /'
        
        # Start service now
        systemctl start "$SERVICE_NAME" 2>&1 | sed 's/^/    /'
        
        # Check status
        if systemctl is-active --quiet "$SERVICE_NAME"; then
            echo "✅ $SERVICE_NAME is running"
        else
            echo "⚠️  $SERVICE_NAME failed to start"
            echo "    Check logs with: journalctl -u $SERVICE_NAME -n 50"
        fi
        
        echo ""
    fi
done

echo "📊 Service Status Summary:"
echo "=========================="
systemctl list-units --type=service | grep venom || echo "No VENOM services found"

echo ""
echo "✅ Installation Complete!"
echo ""
echo "📝 Useful Commands:"
echo "  - Check status:     systemctl status venom-*"
echo "  - View logs:        journalctl -u venom-api.service -f"
echo "  - Stop services:    sudo systemctl stop venom-*"
echo "  - Restart services: sudo systemctl restart venom-*"
echo "  - Disable services: sudo systemctl disable venom-*"
echo ""
echo "🔧 To uninstall, run: sudo ./uninstall-services.sh"
