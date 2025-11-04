#!/bin/bash
# VENOM Mesh Network Deployment Helper
# Deploy VENOM to multiple nodes via SSH

set -e

echo "🌐 VENOM Mesh Network Deployment"
echo "================================="

# Configuration
NODES_FILE="scripts/mesh_nodes.txt"

if [ ! -f "$NODES_FILE" ]; then
    echo "Creating example nodes file..."
    cat > "$NODES_FILE" << 'NODES'
# VENOM Mesh Nodes
# Format: user@hostname
# Example:
# user@node1.local
# user@192.168.1.100
# user@node2.example.com
NODES
    
    echo "❌ No nodes configured. Edit $NODES_FILE and add your nodes."
    exit 1
fi

# Read nodes (skip comments and empty lines)
NODES=$(grep -v '^#' "$NODES_FILE" | grep -v '^$')

if [ -z "$NODES" ]; then
    echo "❌ No nodes configured in $NODES_FILE"
    exit 1
fi

echo "Deploying to nodes:"
echo "$NODES"
echo ""

# Deploy to each node
for NODE in $NODES; do
    echo "📦 Deploying to $NODE..."
    
    # Create directory on remote
    ssh "$NODE" "mkdir -p ~/VENOM-Omega-Lambda"
    
    # Sync files (excluding build artifacts)
    rsync -avz --exclude '.git' \
               --exclude 'build/' \
               --exclude '__pycache__/' \
               --exclude '*.pyc' \
               --exclude 'venv/' \
               . "$NODE:~/VENOM-Omega-Lambda/"
    
    # Install on remote
    ssh "$NODE" "cd ~/VENOM-Omega-Lambda && bash scripts/install_linux.sh"
    
    echo "✅ Deployed to $NODE"
    echo ""
done

echo "✅ Deployment complete!"
echo ""
echo "Start services on each node with:"
echo "  ssh user@node 'systemctl --user start venom-mesh-discovery'"
