
🛰️ **VENOM Ω-Λ API Reference**

> "Lambda is the bridge between entropy and regeneration. Ω-Λ mesh is the digital organism."  
> — manuelstellian-dev

**Version:** 1.0.0-alpha  
**Last Updated:** 2025-01-04  
**Author:** manuelstellian-dev

---

---

## Table of Contents

1. [Overview](#overview)
2. [REST API](#rest-api)
3. [gRPC API](#grpc-api)
4. [Error Handling](#error-handling)
5. [Rate Limits](#rate-limits)
6. [Examples](#examples)

---


## Overview

VENOM provides two parallel APIs for interacting with the Λ-Core:

- **REST API (FastAPI):** Easy-to-use, human-readable JSON. Ideal for web, testing, and simple scripts.  
  **Host:** http://127.0.0.1:8000  
  **Powered by:** venom-api.py

- **gRPC API (Protocol Buffers):** High-performance, low-latency, binary protocol. Ideal for inter-service communication (e.g., Ω ↔ Λ).  
  **Host:** 127.0.0.1:8443  
  **Proto file:** venom.proto

Both APIs expose Lambda mathematical primitives:
• TimeWrap
• Fractal Total
• Möbius Time
• Gravitational Mode

---

---


## REST API (FastAPI)

**Base URL:** `http://127.0.0.1:8000`
**Powered by:** venom-api.py

### **Endpoints**

#### **GET /**

Root endpoint with API information.

**Response**:
```json
{
  "service": "VENOM Λ-Core API",
  "version": "1.0.0",
  "endpoints": {
    "REST": {
      "/time_wrap": "GET - Calculate time wrap",
      "/fractal_total": "GET - Fractal tetrastrat decision",
      "/mobius_time": "GET - Möbius temporal scaling",
      "/grav_mode": "GET - Gravitational mode"
    },
    "gRPC": "localhost:8443"
  }
}
```

---

#### **GET /time_wrap**

Calculate Λ-TimeWrap compression.

**Formula**: `T_Λ = (T1 × ln(U)) / (1 - 1/(kP))`

**Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `k` | float | 100.0 | Scaling factor |
| `p` | float | 10.0 | Pressure factor |
| `u` | float | 1e6 | Utility magnitude |

**Example Request**:
```bash
curl "http://127.0.0.1:8000/time_wrap?k=100&p=10&u=1000000"
```

**Response**:
```json
{
  "TΛ": 13.815510557964274
}
```

**Interpretation**: With k=100, p=10, u=1e6, time is compressed by factor of ~13.8×

---

#### **GET /fractal_total**

Get fractal tetrastrat decision based on state and theta.

**Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `s` | float | inf | State: 1 (Regen), 0 (Neutral), -1 (Entropy), inf (Fallback) |
| `theta` | float | 0.5 | System health (0.0 - 1.0) |

**Example Request**:
```bash
curl "http://127.0.0.1:8000/fractal_total?s=1&theta=0.75"
```

**Response**:
```json
{
  "state": "Regen",
  "ops": ["Scan", "Detect", "Quarantine", "Heal", "Improve", "Reinvest"]
}
```

**States**:

| s | State | Operations |
|---|-------|------------|
| 1 | Regen | Scan, Detect, Quarantine, Heal, Improve, Reinvest |
| 0 | Neutral | Scan, Detect, Quarantine, Heal, Neutralize, Stabilize |
| -1 | Entropy | Reinvest_neg, Degrade, Infect, Spread, Ignore, Blind |
| inf | Fallback | Depends on theta |

---

#### **GET /mobius_time**

Calculate Möbius temporal scaling.

**Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `s` | float | inf | State |
| `theta` | float | 0.5 | System health |
| `k` | float | 100.0 | Scaling factor |
| `p` | float | 10.0 | Pressure factor |
| `u` | float | 1e6 | Utility magnitude |

**Example Request**:
```bash
curl "http://127.0.0.1:8000/mobius_time?s=1&theta=0.85&k=120&p=8&u=2000000"
```

**Response**:
```json
{
  "Möbius": 17.201508234567
}
```

---

#### **GET /grav_mode**

Get gravitational mode (Accelerate/Stagnate/Brake).

**Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `s` | float | inf | State |
| `theta` | float | 0.5 | System health |
| `k` | float | 100.0 | Scaling factor |
| `p` | float | 10.0 | Pressure factor |
| `u` | float | 1e6 | Utility magnitude |

**Example Request**:
```bash
curl "http://127.0.0.1:8000/grav_mode?s=1&theta=0.9"
```

**Response**:
```json
{
  "mode": "Accelerare",
  "value": 13.815510557964274
}
```

**Modes**:

| s | Mode | Description |
|---|------|-------------|
| 1 | Accelerare | Positive acceleration |
| 0 | Stagnare | Neutral (no acceleration) |
| -1 | Frânare | Negative acceleration (brake) |

---

#### **GET /health**

Health check endpoint.

**Example Request**:
```bash
curl "http://127.0.0.1:8000/health"
```

**Response**:
```json
{
  "status": "healthy",
  "service": "venom-api"
}
```

---


## gRPC API (Protocol Buffers)

**Address:** `127.0.0.1:8443`
**Proto file:** venom.proto

### **Service Definition**

```protobuf
service Venom {
  rpc TimeWrap (TimeWrapReq) returns (FloatReply);
  rpc FractalTotal (FractalReq) returns (FractalReply);
  rpc MobiusTime (MobiusReq) returns (FloatReply);
  rpc GravMode (GravReq) returns (GravReply);
}
```

### **Message Types**

#### **TimeWrapReq**

```protobuf
message TimeWrapReq {
  double k = 1;
  double p = 2;
  double u = 3;
}
```

#### **FloatReply**

```protobuf
message FloatReply {
  double value = 1;
}
```

#### **FractalReq**

```protobuf
message FractalReq {
  int32 s = 1;
  double theta = 2;
}
```

#### **FractalReply**

```protobuf
message FractalReply {
  string state = 1;
  repeated string ops = 2;
}
```

#### **MobiusReq**

```protobuf
message MobiusReq {
  int32 s = 1;
  double theta = 2;
  double k = 3;
  double p = 4;
  double u = 5;
}
```

#### **GravReq**

```protobuf
message GravReq {
  int32 s = 1;
  double theta = 2;
  double k = 3;
  double p = 4;
  double u = 5;
}
```

#### **GravReply**

```protobuf
message GravReply {
  string mode = 1;
  double value = 2;
}
```

---


### Python Examples

#### REST API (requests)

```python
import requests

BASE_URL = "http://127.0.0.1:8000"

# Health
response = requests.get(f"{BASE_URL}/health")
print(f"Health: {response.json()}")

# TimeWrap
params = {"k": 120, "p": 8, "u": 2e6}
response = requests.get(f"{BASE_URL}/time_wrap", params=params)
print(f"TimeWrap: {response.json()}")

# Fractal Total
params = {"s": -1, "theta": 0.2}
response = requests.get(f"{BASE_URL}/fractal_total", params=params)
print(f"Fractal Total: {response.json()}")
```

#### gRPC API

Requires generated stubs (`scripts/generate_proto.sh`)

```python
import grpc

# Import generated stubs
try:
  import venom_pb2
  import venom_pb2_grpc
except ImportError:
  print("Error: gRPC stubs not found.")
  print("Run: ./scripts/generate_proto.sh")
  exit(1)

def run_grpc_example():
  print("🛰️  Testing gRPC API...")
  try:
    channel = grpc.insecure_channel('127.0.0.1:8443')
    stub = venom_pb2_grpc.VenomStub(channel)

    # 1. TimeWrap
    request = venom_pb2.TimeWrapReq(k=120, p=8, u=2e6)
    response = stub.TimeWrap(request)
    print(f"  TimeWrap (gRPC): {response.value:.6f}")

    # 2. Fractal Total
    request = venom_pb2.FractalReq(s=-1, theta=0.2)
    response = stub.FractalTotal(request)
    print(f"  FractalTotal (gRPC): State={response.state}, Ops={list(response.ops)}")

    # 3. Grav Mode
    request = venom_pb2.GravReq(s=1, theta=0.9, k=100, p=10, u=1e6)
    response = stub.GravMode(request)
    print(f"  GravMode (gRPC): Mode={response.mode}, Value={response.value:.6f}")

  except grpc.RpcError as e:
    print(f"❌ gRPC Error: {e.details()} (Is the server running?)")
  except Exception as e:
    print(f"❌ Error: {e}")

if __name__ == "__main__":
  run_grpc_example()
```

#### **Kotlin Client**

```kotlin
import io.grpc.ManagedChannelBuilder
import venom.VenomGrpc
import venom.Venom.*

val channel = ManagedChannelBuilder
    .forAddress("127.0.0.1", 8443)
    .usePlaintext()
    .build()

val stub = VenomGrpc.newBlockingStub(channel)

// TimeWrap
val timeWrapReq = TimeWrapReq.newBuilder()
    .setK(100.0)
    .setP(10.0)
    .setU(1e6)
    .build()

val timeWrapResp = stub.timeWrap(timeWrapReq)
println("TimeWrap: ${timeWrapResp.value}")

// Fractal Total
val fractalReq = FractalReq.newBuilder()
    .setS(1)
    .setTheta(0.75)
    .build()

val fractalResp = stub.fractalTotal(fractalReq)
println("State: ${fractalResp.state}")
println("Ops: ${fractalResp.opsList}")

channel.shutdown()
```

---

## Error Handling

### **REST API Errors**

**Error Response Format**:
```json
{
  "detail": "Error message"
}
```

**HTTP Status Codes**:

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request (invalid parameters) |
| 500 | Internal Server Error |

**Example Error**:
```bash
curl "http://127.0.0.1:8000/time_wrap?k=0&p=0"
```

**Response (400)**:
```json
{
  "detail": "k * p must not equal 1"
}
```

### **gRPC Errors**

**Status Codes**:

| Code | Description |
|------|-------------|
| OK | Success |
| INVALID_ARGUMENT | Invalid parameters |
| UNAVAILABLE | Service not running |
| DEADLINE_EXCEEDED | Timeout |

**Example**:
```python
try:
    response = stub.TimeWrap(request, timeout=5)
except grpc.RpcError as e:
    print(f"Error: {e.code()}, {e.details()}")
```

---

## Rate Limits

**Current**: No rate limiting

**Recommended for production**:
- 100 requests/minute per IP
- 1000 requests/hour per IP

**Implementation** (optional):
```python
from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/time_wrap")
@limiter.limit("100/minute")
def time_wrap_endpoint(request: Request, k: float = 100.0):
    # ... implementation
```
