
#!/bin/bash
# scripts/generate_proto.sh
# Supreme Hybrid VENOM gRPC Python Stub Generator
# ---------------------------------------------------
# Păstrează tot codul workspace și adaugă incremental funcționalități avansate

set -e

echo "🔧 Generating gRPC stubs from venom.proto"
echo "=========================================="
echo ""

PROTO_DIR="venom_lambda/core"
OUT_DIR="venom_lambda/core"

# Check if grpcio-tools is installed
if ! python3 -c "import grpc_tools" 2>/dev/null; then
    echo "⚠️  grpcio-tools not found. Installing..."
    pip3 install grpcio-tools
fi

# Generate Python gRPC code (.py, .pyi)
python3 -m grpc_tools.protoc \
    -I"$PROTO_DIR" \
    --python_out="$OUT_DIR" \
    --grpc_python_out="$OUT_DIR" \
    --pyi_out="$OUT_DIR" \
    "$PROTO_DIR/venom.proto"

# Check if generated
if [ -f "$OUT_DIR/venom_pb2.py" ] && [ -f "$OUT_DIR/venom_pb2_grpc.py" ]; then
    echo "✅ Generated files:"
    echo "   - $OUT_DIR/venom_pb2.py"
    echo "   - $OUT_DIR/venom_pb2_grpc.py"
    echo "   - $OUT_DIR/venom_pb2.pyi"
    echo ""
    echo "🎉 gRPC stubs generated successfully!"
else
    echo "❌ Failed to generate stubs"
    exit 1
fi

# Workspace legacy messages (păstrate):
echo "✅ Generated:"
echo "  - ${OUT_DIR}/venom_pb2.py"
echo "  - ${OUT_DIR}/venom_pb2_grpc.py"
