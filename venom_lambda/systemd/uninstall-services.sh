
#!/bin/bash
# VENOM Λ-GENESIS Systemd Services Uninstallation Script (Hibrid)
# Oprește, dezactivează și elimină toate serviciile VENOM Lambda (user-level și root)

set -e  # Exit on error

echo "� VENOM Λ-GENESIS Service Uninstallation"
echo "=========================================="

# Detect user-level sau root
if [ "$EUID" -ne 0 ]; then
    echo "🔧 User-level uninstall (systemctl --user)"
    SYSTEMCTL="systemctl --user"
    SERVICE_DIR="$HOME/.config/systemd/user"
else
    echo "🔧 Root uninstall (systemctl)"
    SYSTEMCTL="systemctl"
    SERVICE_DIR="/etc/systemd/system"
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
    SERVICE_PATH="$SERVICE_DIR/$SERVICE"
    if [ -f "$SERVICE_PATH" ]; then
        echo "🛑 Stopping $SERVICE..."
        if $SYSTEMCTL is-active --quiet "$SERVICE"; then
            $SYSTEMCTL stop "$SERVICE" 2>&1 | sed 's/^/    /'
            echo "✅ $SERVICE stopped"
        else
            echo "⚪ $SERVICE was not running"
        fi
        if $SYSTEMCTL is-enabled --quiet "$SERVICE" 2>/dev/null; then
            $SYSTEMCTL disable "$SERVICE" 2>&1 | sed 's/^/    /'
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
for SERVICE in "${SERVICES[@]}"; do
    SERVICE_PATH="$SERVICE_DIR/$SERVICE"
    if [ -f "$SERVICE_PATH" ]; then
        echo "🗑️  Removing $SERVICE..."
        rm -f "$SERVICE_PATH"
        echo "✅ $SERVICE removed"
    fi
done

echo ""
echo "🔄 Reloading systemd daemon..."
$SYSTEMCTL daemon-reload
if [ "$EUID" -eq 0 ]; then
    $SYSTEMCTL reset-failed 2>/dev/null || true
fi

echo ""
echo "📊 Verifying removal..."
if [ "$EUID" -ne 0 ]; then
    REMAINING=$($SYSTEMCTL list-units --type=service --all | grep venom | wc -l)
else
    REMAINING=$($SYSTEMCTL list-units --type=service --all | grep venom | wc -l)
fi

if [ "$REMAINING" -eq 0 ]; then
    echo "✅ All VENOM services successfully removed"
else
    echo "⚠️  Some VENOM services may still be present:"
    $SYSTEMCTL list-units --type=service --all | grep venom || true
fi

echo ""
echo "✅ Uninstallation Complete!"
echo ""
echo "📝 Note: Service logs are still available in journalctl"
echo "   To view old logs: journalctl -u venom-api.service"
echo ""
echo "🔧 To reinstall, run: ./install-services.sh (user) sau sudo ./install-services.sh (root)"
