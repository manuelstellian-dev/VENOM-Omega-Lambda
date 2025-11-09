
#!/bin/bash
# VENOM Λ-GENESIS Systemd Services Installation Script (Hibrid)
# Instalează și activează toate serviciile VENOM Lambda (user-level și root)

set -e  # Exit on error

echo "� VENOM Λ-GENESIS Service Installation"
echo "========================================"

# Detect user-level sau root
if [ "$EUID" -ne 0 ]; then
    echo "🔧 User-level install (systemctl --user)"
    SYSTEMCTL="systemctl --user"
    SERVICE_DIR="$HOME/.config/systemd/user"
else
    echo "🔧 Root install (systemctl)"
    SYSTEMCTL="systemctl"
    SERVICE_DIR="/etc/systemd/system"
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
    cp "$SERVICE_FILE" "$SERVICE_DIR/"
    sed -i "s|/path/to/venom|$VENOM_ROOT|g" "$SERVICE_DIR/$SERVICE"
    echo "✅ $SERVICE installed"
done

echo ""
echo "🔄 Reloading systemd daemon..."
$SYSTEMCTL daemon-reload

echo ""
echo "🚀 Enabling and starting services..."
echo ""

# Enable and start each service
for SERVICE in "${SERVICES[@]}"; do
    SERVICE_NAME="${SERVICE}"
    if [ -f "$SERVICE_DIR/$SERVICE_NAME" ]; then
        echo "▶️  Starting $SERVICE_NAME..."
        $SYSTEMCTL enable "$SERVICE_NAME" 2>&1 | sed 's/^/    /'
        $SYSTEMCTL start "$SERVICE_NAME" 2>&1 | sed 's/^/    /'
        if $SYSTEMCTL is-active --quiet "$SERVICE_NAME"; then
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
$SYSTEMCTL list-units --type=service | grep venom || echo "No VENOM services found"

echo ""
echo "✅ Installation Complete!"
echo ""
echo "📝 Useful Commands:"
if [ "$EUID" -ne 0 ]; then
    echo "  - Check status:     systemctl --user status venom-*"
    echo "  - View logs:        journalctl --user -u venom-api.service -f"
    echo "  - Stop services:    systemctl --user stop venom-*"
    echo "  - Restart services: systemctl --user restart venom-*"
    echo "  - Disable services: systemctl --user disable venom-*"
    echo "  - Uninstall:        ./uninstall-services.sh"
else
    echo "  - Check status:     systemctl status venom-*"
    echo "  - View logs:        journalctl -u venom-api.service -f"
    echo "  - Stop services:    sudo systemctl stop venom-*"
    echo "  - Restart services: sudo systemctl restart venom-*"
    echo "  - Disable services: sudo systemctl disable venom-*"
    echo "  - Uninstall:        sudo ./uninstall-services.sh"
fi
echo ""
