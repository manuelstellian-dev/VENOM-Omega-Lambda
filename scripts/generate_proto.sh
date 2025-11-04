#!/bin/bash
# Generate Python gRPC code from proto files

set -e

echo "🔧 Generating gRPC code from proto files..."

PROTO_DIR="lambda/core"
OUT_DIR="lambda/core"

# Check if grpcio-tools is installed
if ! python3 -c "import grpc_tools" 2>/dev/null; then
    echo "Installing grpcio-tools..."
    pip3 install grpcio-tools
fi

# Generate Python gRPC code
python3 -m grpc_tools.protoc \
    -I"$PROTO_DIR" \
    --python_out="$OUT_DIR" \
    --grpc_python_out="$OUT_DIR" \
    "$PROTO_DIR/venom.proto"

echo "✅ Generated:"
echo "  - ${OUT_DIR}/venom_pb2.py"
echo "  - ${OUT_DIR}/venom_pb2_grpc.py"
