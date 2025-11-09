
#!/bin/bash
# scripts/install_linux.sh
# Supreme Hybrid VENOM Λ-CORE Linux Installation Script
# ---------------------------------------------------
# Păstrează tot codul workspace și adaugă incremental funcționalități avansate

set -e

echo "🐧 VENOM Λ-CORE Linux Installation Script"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.8"

if ! python3 -c 'import sys; exit(0 if sys.version_info >= (3, 8) else 1)'; then
    echo -e "${RED}❌ Error: Python 3.8+ required. Found: $PYTHON_VERSION${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}"

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip3 install --user -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi

# Generate gRPC stubs
echo ""
echo "🔧 Generating gRPC stubs..."
cd lambda/core
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. venom.proto
cd ../..

if [ -f "lambda/core/venom_pb2.py" ]; then
    echo -e "${GREEN}✅ gRPC stubs generated${NC}"
else
    echo -e "${RED}❌ Failed to generate gRPC stubs${NC}"
    exit 1
fi

# Create directories (supreme set)
echo ""
echo "📁 Creating directories..."
mkdir -p ~/venom/logs
mkdir -p ~/venom/lambda/core
mkdir -p ~/venom/lambda/arbiter_core
mkdir -p ~/venom/lambda/organs
mkdir -p ~/venom/lambda/pulse
mkdir -p ~/venom/lambda/mesh
mkdir -p ~/.config/systemd/user

echo -e "${GREEN}✅ Directories created${NC}"

# Copy Lambda files (supreme)
echo ""
echo "📋 Copying Lambda files..."
cp -r lambda/* ~/venom/lambda/

echo -e "${GREEN}✅ Files copied${NC}"

# Install systemd services
echo ""
echo "🔧 Installing systemd services..."
cp systemd/*.service ~/.config/systemd/user/
systemctl --user daemon-reload

echo -e "${GREEN}✅ Systemd services installed${NC}"

# Enable and start services
echo ""
echo "🚀 Starting services..."
systemctl --user enable venom-fractal.service
systemctl --user enable venom-api.service
systemctl --user enable venom-mesh-discovery.service
systemctl --user enable venom-mesh-orchestrator.service

systemctl --user start venom-fractal.service
systemctl --user start venom-api.service
systemctl --user start venom-mesh-discovery.service
systemctl --user start venom-mesh-orchestrator.service

echo -e "${GREEN}✅ Services started${NC}"

# Check status
echo ""
echo "📊 Service Status:"
systemctl --user status venom-fractal.service --no-pager | head -5
systemctl --user status venom-api.service --no-pager | head -5

echo ""
echo -e "${GREEN}🎉 Installation complete!${NC}"
echo ""
echo "The Lambda organism is now alive on your system."
echo ""
echo "Useful commands:"
echo "  - View logs: journalctl --user -u venom-fractal.service -f"
echo "  - Stop all: systemctl --user stop venom-*.service"
echo "  - Restart: systemctl --user restart venom-*.service"
echo "  - Test API: curl http://127.0.0.1:8000/health"
echo ""
# Workspace legacy commands (păstrate):
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
