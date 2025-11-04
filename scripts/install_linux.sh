#!/bin/bash
# VENOM Λ-Genesis Linux Installation Script

set -e

echo "🌌 VENOM Λ-Genesis Linux Installation"
echo "======================================"

# Check Python version
echo ""
echo "Checking Python version..."
python3 --version

if ! python3 -c 'import sys; exit(0 if sys.version_info >= (3, 8) else 1)'; then
    echo "❌ Python 3.8 or higher required"
    exit 1
fi

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip3 install --user -r requirements.txt

echo ""
echo "Installing VENOM lambda package..."
pip3 install --user -e .

# Install systemd services
echo ""
echo "Installing systemd services..."
mkdir -p ~/.config/systemd/user

cp venom_lambda/systemd/*.service ~/.config/systemd/user/

# Update WorkingDirectory in service files
REPO_DIR=$(pwd)
for service in ~/.config/systemd/user/venom-*.service; do
    sed -i "s|WorkingDirectory=%h/VENOM-Omega-Lambda|WorkingDirectory=$REPO_DIR|g" "$service"
done

# Reload systemd
systemctl --user daemon-reload

echo ""
echo "✅ Installation complete!"
echo ""
echo "Available services:"
echo "  venom-fractal"
echo "  venom-api"
echo "  venom-mesh-discovery"
echo "  venom-mesh-orchestrator"
echo ""
echo "Enable and start services with:"
echo "  systemctl --user enable --now venom-api"
echo ""
echo "Check status with:"
echo "  systemctl --user status venom-api"
