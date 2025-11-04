# Λ-Genesis Architecture

## Organ System (Python)

### Core Components

#### 1. LambdaArbiter
- **Purpose**: Central coordinator
- **Genome**: JSON config with R,B,E,O weights
- **time_wrap()**: Apply temporal transformation
- **recalibrate()**: Adjust from organ feedback

#### 2. Organs

**RegenCore (R) - Regeneration**
- Detect damage
- Quarantine threats
- Improve systems
- Reinvest resources

**BalanceCore (B) - Balance**
- Stabilize allocation
- Conserve energy
- Maintain equilibrium

**EntropyCore (E) - Entropy**
- Self-attack testing
- Detect threats
- Defend systems
- Learn patterns

**OptimizeCore (O) - Optimization**
- Detect targets
- Adjust parameters
- Redistribute resources
- Trigger restarts

#### 3. PulseFractal
- **Purpose**: Organism heartbeat
- **Frequency**: ~1ms (1000Hz)
- **Synchronization**: Coordinates all organs

#### 4. Mesh Network
- **Nodes**: NanoBots with roles
  - memory_carrier
  - signal_relay
  - knowledge_keeper
  - generic
- **Communication**: Broadcast and direct delivery
- **Discovery**: UDP multicast (224.1.1.1:19845)
- **Orchestration**: Load-balanced task dispatch

#### 5. Core Functions (fractal.py)

**time_wrap()**
```python
T_wrap = T1 / (k × (1 + ln(1 + p)) × (1 + u))
```

**fractal_total()**
```python
Θ(θ) = 1 + ln(1 + θ)
Total = s × Θ(θ)
```

**mobius_time()**
```python
speedup = fractal_total(k × p, θ)
compressed = s / speedup
```

**grav_mode()**
```python
Returns: {original, compressed, speedup, efficiency}
```

#### 6. Services

**FastAPI (venom_api.py)**
- REST endpoints: /time_wrap, /fractal_total, /mobius_time, /grav_mode
- Port: 8000 (configurable)
- Bind: 127.0.0.1 (localhost)

**gRPC (venom.proto)**
- Service: VenomService
- Methods: TimeWrap, FractalTotal, MobiusTime, GravMode

**Mesh Discovery (mesh_discovery.py)**
- UDP multicast announcements
- Peer tracking and cleanup
- Saves to ~/.venom_peers.json

**Mesh Orchestrator (venom_mesh_orchestrator.py)**
- Load peers from discovery
- Health check nodes
- Dispatch tasks to least-loaded
- EMA-based load tracking

## Deployment

Use systemd services for persistent operation:
- venom-fractal.service
- venom-api.service
- venom-mesh-discovery.service
- venom-mesh-orchestrator.service
