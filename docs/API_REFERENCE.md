# VENOM API Reference

## REST API (FastAPI)

**Base URL**: `http://127.0.0.1:8000`

### Endpoints

#### POST /time_wrap
Apply time wrapping transformation

**Request**:
```json
{
  "k": 1.5,
  "p": 0.75,
  "u": 0.2,
  "t1": 1000.0
}
```

**Response**:
```json
{
  "wrapped_time": 250.5,
  "original": 1000.0,
  "compression_ratio": 3.99
}
```

#### POST /fractal_total
Calculate fractal total speedup

**Request**:
```json
{
  "s": 5.0,
  "theta": 0.7
}
```

**Response**:
```json
{
  "total_speedup": 8.52,
  "sequential": 5.0,
  "theta": 0.7
}
```

#### POST /mobius_time
Möbius time compression

**Request**:
```json
{
  "s": 1000.0,
  "k": 1.5,
  "p": 0.75,
  "u": 0.2,
  "theta": 0.7
}
```

#### POST /grav_mode
Gravitational mode calculation

**Response**:
```json
{
  "original": 1000.0,
  "compressed": 185.2,
  "speedup": 5.40,
  "theta": 0.7,
  "efficiency": 4.80
}
```

## gRPC API

See `lambda/core/venom.proto` for service definition.

Generate client code:
```bash
bash scripts/generate_proto.sh
```

## Kotlin API

### VenomOrganism

```kotlin
val organism = VenomOrganism.getInstance(context)

// Initialize
organism.birth()

// Get vitals
val vitals = organism.getVitals()

// Interact
val response = organism.interact("query")

// Shutdown
organism.shutdown()
```

## Python API

### Lambda Arbiter

```python
from lambda.arbiter_core import LambdaArbiter

arbiter = LambdaArbiter()
result = arbiter.time_wrap(health_data)
```

### Mesh Network

```python
from lambda.mesh import Mesh

mesh = Mesh()
mesh.add_node("node-1", "generic")
mesh.broadcast("node-1", data)
```
