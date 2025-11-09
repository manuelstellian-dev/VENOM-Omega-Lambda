
#!/bin/bash
# scripts/deploy_mesh.sh
# Supreme Hybrid VENOM Mesh Multi-Device Deployment Script
# ---------------------------------------------------
# Păstrează tot codul workspace și adaugă incremental funcționalități avansate

set -e

echo "🕸️  VENOM Mesh Multi-Device Deployment"
echo "======================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
DEVICES_FILE="mesh_devices.txt"
NODES_FILE="scripts/mesh_nodes.txt"

# Check if devices file exists (supreme)
if [ ! -f "$DEVICES_FILE" ]; then
    echo "Creating default mesh_devices.txt..."
    cat > "$DEVICES_FILE" << EOF
# VENOM Mesh Devices
# Format: user@hostname (one per line)
# Example:
# user@192.168.1.100
# user@desktop-pc
# user@laptop
EOF
    echo "⚠️  Please edit mesh_devices.txt and add your devices"
    echo "Then run this script again."
    exit 0
fi

# Read devices
mapfile -t DEVICES < <(grep -v '^#' "$DEVICES_FILE" | grep -v '^$')

if [ ${#DEVICES[@]} -eq 0 ]; then
    echo "❌ No devices found in $DEVICES_FILE"
    exit 1
fi

echo "Found ${#DEVICES[@]} device(s):"
for device in "${DEVICES[@]}"; do
    echo "  - $device"
done
echo ""

# Deploy to each device
for device in "${DEVICES[@]}"; do
    echo "� Deploying to $device..."
    
    # Check SSH connection
    if ! ssh -o ConnectTimeout=5 "$device" "echo connected" &>/dev/null; then
        echo "❌ Cannot connect to $device. Skipping..."
        continue
    fi
    
    # Create directories
    ssh "$device" "mkdir -p ~/venom/lambda"
    
    # Copy Lambda files
    echo "   Copying files..."
    scp -r lambda/* "$device:~/venom/lambda/"
    scp requirements.txt "$device:~/venom/"
    scp -r systemd "$device:~/venom/"
    
    # Install dependencies
    echo "   Installing dependencies..."
    ssh "$device" "cd ~/venom && pip3 install --user -r requirements.txt"
    
    # Generate proto
    echo "   Generating gRPC stubs..."
    ssh "$device" "cd ~/venom/lambda/core && python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. venom.proto"
    
    # Install systemd services
    echo "   Installing systemd services..."
    ssh "$device" "cp ~/venom/systemd/*.service ~/.config/systemd/user/"
    ssh "$device" "systemctl --user daemon-reload"
    
    # Start services
    echo "   Starting services..."
    ssh "$device" "systemctl --user restart venom-fractal.service"
    ssh "$device" "systemctl --user restart venom-api.service"
    ssh "$device" "systemctl --user restart venom-mesh-discovery.service"
    ssh "$device" "systemctl --user restart venom-mesh-orchestrator.service"
    
    echo "✅ Deployed to $device"
    echo ""
done

echo "🎉 Mesh deployment complete!"
echo ""
echo "The mesh is now discovering peers..."
echo "Wait 10 seconds and check: cat ~/.venom_peers.json"
echo ""
# Workspace legacy deployment (păstrat):
echo "Deploying to nodes:"
echo "$NODES"
echo ""
for NODE in $NODES; do
    echo "📦 Deploying to $NODE..."
    ssh "$NODE" "mkdir -p ~/VENOM-Omega-Lambda"
    rsync -avz --exclude '.git' \
               --exclude 'build/' \
               --exclude '__pycache__/' \
               --exclude '*.pyc' \
               --exclude 'venv/' \
               . "$NODE:~/VENOM-Omega-Lambda/"
    ssh "$NODE" "cd ~/VENOM-Omega-Lambda && bash scripts/install_linux.sh"
    echo "✅ Deployed to $NODE"
    echo ""
done
echo "✅ Deployment complete!"
echo ""
echo "Start services on each node with:"
echo "  ssh user@node 'systemctl --user start venom-mesh-discovery'"
