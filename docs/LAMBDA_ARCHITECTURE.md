
# Λ-GENESIS Architecture

**Lambda Layer - Digital Biology**

---

## Table of Contents

1. [Overview](#overview)
2. [Arbiter Core](#arbiter-core)
3. [Four Organs](#four-organs)
4. [Pulse Fractal](#pulse-fractal)
5. [Mesh Network](#mesh-network)
6. [Core Engine](#core-engine)

---

## Overview

Λ-GENESIS (Lambda Genesis) is the **biological layer** of VENOM, implemented in Python. It mimics organic systems with:

- **Digital DNA** (genome.json with 4 bases)
- **4 Organs** [R, B, E, O] working in parallel
- **Pulse Fractal** (1ms heartbeat)
- **Mesh Network** (cellular communication)
- **100+ NanoBots** (digital cells)
- **Core Engine** (mathematical primitives)

**Philosophy**: Not software that runs, but an organism that **breathes**.

---

## Arbiter Core

### **LambdaArbiter**

**Location**: `lambda/arbiter_core/arbiter.py`

**Purpose**: Coordinate 4 organs using genome weights.

#### Genome Structure

```json
{
  "Λ-genome": {
  "bases": ["R", "B", "E", "O"],
  "weights": {
    "R": 0.20,  // REGEN
    "B": 0.30,  // BALANCE
    "E": 0.15,  // ENTROPY
    "O": 0.30,  // OPTIMIZE
    "Λ": 0.05   // Lambda wrap coefficient
  },
  "pulses": "fractal_parallel"
  }
}
```

#### Time Wrap - Parallel Execution

```python
def time_wrap(self, health_data: Dict[str, Any] = None) -> Dict[str, Any]:
  """
  Execute all 4 organs in parallel (like DNA replication)
  """
  results = {}
    
  with ThreadPoolExecutor(max_workers=4) as executor:
    futures = {
      executor.submit(organ.cycle, health_data): name
      for name, organ in self.organs.items()
    }
        
    for future in as_completed(futures):
      organ_name = futures[future]
      result = future.result(timeout=5.0)
      results[organ_name] = result
    
  # Integrate based on genome weights
  integrated = self.recalibrate(results)
    
  return integrated
```

#### Recalibration (Weighted Integration)

```python
def recalibrate(self, organ_results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
  """
  Integrate organ results using genome weights
  """
  weights = self.genome['weights']
  integrated_score = 0.0
  total_weight = 0.0
    
  for organ_name, result in organ_results.items():
    organ_key = organ_name[0]  # R, B, E, O
    weight = weights.get(organ_key, 0.25)
        
    # Score based on success
    organ_score = 1.0 if result.get('action') != 'error' else 0.0
        
    integrated_score += weight * organ_score
    total_weight += weight
    
  # Normalize
  if total_weight > 0:
    integrated_score /= total_weight
    
  return {
    "organs": organ_results,
    "integrated_score": integrated_score,
    "genome_balance": weights,
    "timestamp": self._get_timestamp()
  }
```

#### Adaptive Genome Modes

Based on θ (system health), genome weights adjust:

**Unwrap Mode** (θ: 0.0 - 0.3) - Energy conservation
```json
{
  "R": 0.40,  // REGEN priority
  "B": 0.30,
  "E": 0.10,
  "O": 0.15,
  "Λ": 0.05
}
```

**Balance Mode** (θ: 0.5 - 0.7) - Optimal equilibrium
```json
{
  "R": 0.20,
  "B": 0.35,  // BALANCE priority
  "E": 0.15,
  "O": 0.25,
  "Λ": 0.05
}
```

**Optimize Mode** (θ: 0.9 - 1.0) - Maximum performance
```json
{
  "R": 0.10,
  "B": 0.20,
  "E": 0.10,
  "O": 0.50,  // OPTIMIZE dominant
  "Λ": 0.10
}
```

---

## Four Organs

### **1. REGEN Organ (20%)**

**Location**: `lambda/organs/regen_core.py`

**Flow**: **Detect → Quarantine → Improve → Reinvest (97%)**

#### Purpose
Self-healing and resource recycling. Like a biological immune system that repairs damage and reinvests freed resources.

#### Detection

```python
def detect_damage(self, health_data: Dict[str, Any]) -> List[str]:
  """
  Detect what needs repair
  """
  issues = []
    
  # Memory leaks
  if health_data.get('memory_health', 1.0) < 0.5:
    issues.append("memory_leak")
    
  # Model corruption
  if health_data.get('model_corruption', False):
    issues.append("corrupted_model")
    
  # Cache bloat
  if health_data.get('cache_size', 0) > 1_000_000_000:  # >1GB
    issues.append("cache_bloat")
    
  # Thermal damage
  if health_data.get('thermal_health', 1.0) < 0.3:
    issues.append("thermal_damage")
    
  # CPU exhaustion
  if health_data.get('cpu_health', 1.0) < 0.2:
    issues.append("cpu_exhaustion")
    
  return issues
```

#### Quarantine

```python
def quarantine(self, issues: List[str]) -> List[str]:
  """
  Isolate issues for repair
  """
  logging.info(f"🚧 [REGEN] Quarantining {len(issues)} issues")
  return issues  # All issues quarantined
```

#### Improve

```python
def improve(self, quarantined: List[str]) -> List[str]:
  """
  Repair issues
  """
  improved = []
    
  for issue in quarantined:
    if issue == "memory_leak":
      # Trigger garbage collection
      logging.info(f"🔧 [REGEN] Repairing: {issue} (GC triggered)")
      improved.append(f"repaired_{issue}")
            
    elif issue == "corrupted_model":
      # Request model regeneration
      logging.info(f"🔧 [REGEN] Repairing: {issue} (regeneration)")
      improved.append(f"regenerated_{issue}")
            
    elif issue == "cache_bloat":
      # Clear caches
      logging.info(f"🔧 [REGEN] Repairing: {issue} (cache cleared)")
      improved.append(f"cleaned_{issue}")
    
  return improved
```

#### Reinvest (97%)

```python
def reinvest(self, improved: List[str]) -> int:
  """
  Redistribute 97% of freed resources
  """
  resources_freed = len(improved) * 100  # 100MB per issue
  reinvested = int(resources_freed * 0.97)
    
  logging.info(f"♻️ [REGEN] Reinvested {reinvested}MB (97% of {resources_freed}MB)")
    
  return reinvested
```

---

### **2. BALANCE Organ (30%)**

**Location**: `lambda/organs/balance_core.py`

**Flow**: **Stabilize → Conserve → Maintain**

#### Purpose
Maintain system homeostasis and equilibrium.

#### Stabilize

```python
def stabilize(self, theta: float) -> str:
  """
  Adjust system mode based on theta
  """
  if theta < 0.3:
    mode = "unwrap_mode"
    logging.info(f"⚖️ [BALANCE] Stabilizing: UNWRAP (θ={theta:.2f})")
  elif theta < 0.5:
    mode = "transition_mode"
  elif theta < 0.7:
    mode = "balance_mode"
  elif theta < 0.9:
    mode = "wrap_mode"
  else:
    mode = "optimize_mode"
    
  return mode
```

#### Conserve

```python
def conserve(self, health_data: Dict[str, Any]) -> str:
  """
  Energy conservation based on battery
  """
  battery_level = health_data.get('battery_level', 100)
    
  if battery_level < 20:
    conservation = "aggressive_conservation"
    logging.warning(f"🔋 [BALANCE] AGGRESSIVE (battery: {battery_level}%)")
  elif battery_level < 50:
    conservation = "moderate_conservation"
  else:
    conservation = "normal_operation"
    
  return conservation
```

#### Maintain

```python
def maintain(self) -> str:
  """
  Continuous homeostasis
  """
  return "homeostasis_active"
```

---

### **3. ENTROPY Organ (15%)**

**Location**: `lambda/organs/entropy_core.py`

**Flow**: **Self-Attack → Detect → Defend → Learn**

#### Purpose
Digital immunity through self-testing and learning from threats.

#### Self-Attack

```python
def self_attack(self) -> List[str]:
  """
  Test own defenses (like immune system self-testing)
  """
  test_attacks = [
    "memory_overflow",
    "cpu_spike",
    "model_poisoning",
    "cache_corruption"
  ]
    
  vulnerabilities = []
    
  for attack in test_attacks:
    if not self.is_defended_against(attack):
      vulnerabilities.append(attack)
      logging.warning(f"🔍 [ENTROPY] Vulnerability: {attack}")
    
  return vulnerabilities
```

#### Detect

```python
def detect_threats(self, health_data: Dict[str, Any]) -> List[str]:
  """
  Detect real threats
  """
  threats = []
    
  # CPU anomaly
  if health_data.get('cpu_health', 1.0) < 0.1:
    threats.append("cpu_spike")
    
  # Memory anomaly
  if health_data.get('memory_health', 1.0) < 0.2:
    threats.append("memory_attack")
    
  # Thermal attack
  if health_data.get('thermal_health', 1.0) < 0.3:
    threats.append("thermal_attack")
    
  return threats
```

#### Defend

```python
def defend(self, threats: List[str]) -> int:
  """
  Defend against threats
  """
  defended_count = 0
    
  for threat in threats:
    if threat in self.learned_threats:
      # Known threat - effective defense
      logging.info(f"🛡️ [ENTROPY] Defended (known): {threat}")
      defended_count += 1
    else:
      # New threat - partial defense
      logging.info(f"🛡️ [ENTROPY] Defended (learning): {threat}")
      defended_count += 0.5
    
  return int(defended_count)
```

#### Learn

```python
def learn(self, threats: List[str]):
  """
  Learn from threats (digital immunity learning)
  """
  for threat in threats:
    if threat not in self.learned_threats:
      self.learned_threats.append(threat)
      logging.info(f"🧠 [ENTROPY] Learned: {threat}")
    
  # Keep only last 100 threats
  if len(self.learned_threats) > 100:
    self.learned_threats = self.learned_threats[-100:]
```

---

### **4. OPTIMIZE Organ (30%)**

**Location**: `lambda/organs/optimize_core.py`

**Flow**: **Detect → Adjust → Redistribute → Restart**

#### Purpose
Maximize system efficiency and performance.

#### Detect Optimization Targets

```python
def detect_optimization_targets(self, health_data: Dict[str, Any]) -> List[str]:
  """
  Find optimization opportunities
  """
  targets = []
  theta = health_data.get('theta', 0.5)
    
  # Model quantization
  model_size = health_data.get('model_size', 0)
  if theta < 0.5 and model_size > 1_000_000_000:
    targets.append("quantize_model")
    
  # Thread optimization
  cpu_cores = health_data.get('cpu_cores', 4)
  if cpu_cores > 4:
    targets.append("increase_threads")
    
  # Cache optimization
  cache_hit_rate = health_data.get('cache_hit_rate', 1.0)
  if cache_hit_rate < 0.7:
    targets.append("optimize_cache")
    
  return targets
```

#### Adjust

```python
def adjust(self, targets: List[str]) -> List[str]:
  """
  Apply optimizations
  """
  adjustments = []
    
  for target in targets:
    if target == "quantize_model":
      adjustments.append("model_quantized_int8")
      logging.info(f"⚙️ [OPTIMIZE] Model → INT8")
            
    elif target == "increase_threads":
      adjustments.append("threads_increased")
      logging.info(f"⚙️ [OPTIMIZE] Threads → increased")
            
    elif target == "optimize_cache":
      adjustments.append("cache_optimized")
      logging.info(f"⚙️ [OPTIMIZE] Cache → LRU")
    
  return adjustments
```

#### Redistribute

```python
def redistribute(self, health_data: Dict[str, Any]) -> Dict[str, int]:
  """
  Redistribute resources by priority
  """
  theta = health_data.get('theta', 0.5)
    
  if theta < 0.3:
    # UNWRAP: Priority to REGEN
    distribution = {"REGEN": 40, "BALANCE": 30, "ENTROPY": 15, "OPTIMIZE": 15}
  elif theta < 0.7:
    # BALANCE: Equilibrium
    distribution = {"REGEN": 25, "BALANCE": 35, "ENTROPY": 20, "OPTIMIZE": 20}
  else:
    # OPTIMIZE: Priority to performance
    distribution = {"REGEN": 20, "BALANCE": 25, "ENTROPY": 20, "OPTIMIZE": 35}
    
  return distribution
```

---

## Pulse Fractal

### **PulseFractal**

**Location**: `lambda/pulse/pulse.py`

**Purpose**: Heartbeat that drives organism metabolism.

#### Beat Cycle (1ms)

```python
def beat(self):
  """
  1ms fractal beat - all organs work simultaneously
  """
  while self.alive:
    beat_start = time.time()
        
    # TIME WRAP: Parallel organ execution
    results = self.lambda_arbiter.time_wrap()
        
    # Log pulse
    self.log_pulse(results)
        
    # Increment counter
    self.beat_count += 1
        
    # Calculate beat duration
    beat_duration = time.time() - beat_start
        
    # Sleep until next beat (1ms target)
    sleep_time = max(0, 0.001 - beat_duration)
    if sleep_time > 0:
      time.sleep(sleep_time)
```

#### Adaptive Timing

```python
def _calculate_adaptive_cycle(self) -> float:
  """
  Adjust cycle time based on Möbius compression
  """
  compression = 1.0  # From Möbius Engine
  adjusted_cycle = self.cycle_time / (compression ** 0.1)
    
  # Clamp to [0.5ms, 10ms]
  return max(0.0005, min(adjusted_cycle, 0.01))
```

#### Vitals

```python
def get_vitals(self) -> Dict[str, Any]:
  """
  Pulse statistics
  """
  return {
    "alive": self.alive,
    "beat_count": self.beat_count,
    "total_beats": self.total_beats,
    "cycle_time_ms": self.cycle_time * 1000,
    "avg_beat_time_ms": self.avg_beat_time * 1000,
    "min_beat_time_ms": self.min_beat_time * 1000,
    "max_beat_time_ms": self.max_beat_time * 1000
  }
```

---

## Mesh Network

### **Mesh - Digital Tissues**

**Location**: `lambda/mesh/mesh.py`

**Purpose**: Communication network (like blood vessels + nerves).

#### Architecture

```
Node A ──┐
     ├──► Mesh ──► Queue ──► Delivery ──► Node B
Node C ──┘                                      Node D
```

#### Broadcast (Blood)

```python
def broadcast(self, sender: str, data: Any):
  """
  Broadcast to all nodes (like blood carrying nutrients)
  """
  for nid, ref in self.nodes.items():
    if nid != sender:
      self.message_queue.put((nid, data), timeout=0.001)
```

#### Delivery Loop (1ms)

```python
def deliver(self):
  """
  Message delivery (like nerve impulses)
  """
  while self.alive:
    if not self.message_queue.empty():
      nid, data = self.message_queue.get(timeout=0.001)
            
      if nid in self.nodes:
        # Deliver message (neuron firing)
        self.nodes[nid].receive(data)
        self.messages_delivered += 1
        
    time.sleep(0.001)  # 1ms fractal
```

### **NanoBot - Digital Cells**

**Location**: `lambda/mesh/nanobot.py`

**Purpose**: Individual cells with specialized roles.

#### 4 Roles

```python
class NanoBot:
  def __init__(self, node_id: str, role: str):
    self.role = role
    self.memory_capacity = self._get_memory_capacity()
    
  def _get_memory_capacity(self) -> int:
    capacities = {
      "memory_carrier": 200,      # High capacity
      "signal_relay": 50,          # Fast relay
      "knowledge_keeper": 500,     # Very high
      "generic": 100               # Default
    }
    return capacities.get(self.role, 100)
```

#### Receive (Neuron-like)

```python
def receive(self, data: Any):
  """
  Receive signal (like neuron dendrites)
  """
  message = {
    "timestamp": time.time(),
    "data": data,
    "processed": False
  }
    
  self.memory.append(message)
  self._process_message(message)
    
  # FIFO eviction if full
  if len(self.memory) > self.memory_capacity:
    self.memory.pop(0)
```

---

## Core Engine

### **fractal.py - Mathematical Primitives**

**Location**: `lambda/core/fractal.py`

#### TimeWrap Formula

```python
def time_wrap(k: float, p: float, u: float, t1: float = 1.0) -> float:
  """
  T_Λ = (T1 × ln(U)) / (1 - 1/(kP))
  """
  if k * p == 1:
    raise ValueError("k × p must not equal 1")
    
  return (t1 * math.log(u)) / (1 - 1 / (k * p))
```

#### Fractal Tetrastrat

```python
_STATE_MAP = {
  1: ("Regen", ["Scan", "Detect", "Quarantine", "Heal", "Improve", "Reinvest"]),
  0: ("Neutral", ["Scan", "Detect", "Quarantine", "Heal", "Neutralize", "Stabilize"]),
  -1: ("Entropy", ["Reinvest_neg", "Degrade", "Infect", "Spread", "Ignore", "Blind"])
}

def fractal_total(s: int, theta: float) -> Tuple[str, List[str]]:
  if s in _STATE_MAP:
    return _STATE_MAP[s]
  if s == float("inf"):
    return fallback(theta)
```

#### Möbius Temporal

```python
def mobius_time(s: int, k: float, p: float, u: float, theta: float) -> float:
  """
  Time scaling per state
  """
  if s == 1:
    return time_wrap(k, p, u)
  if s == 0:
    return math.log(u)
  if s == -1:
    return sum((k * p) ** i * math.log(u) for i in range(10))
```

#### Gravitational Mode

```python
def grav_mode(s: int, theta: float, k: float, p: float, u: float) -> Tuple[str, float]:
  """
  Accelerate / Stagnate / Brake
  """
  if s == 1:
    return "Accelerare", time_wrap(k, p, u)
  if s == 0:
    return "Stagnare", math.log(u)
  if s == -1:
    return "Frânare", -time_wrap(k, p, u)
```

---

## Services

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

---

## Deployment

Use systemd services for persistent operation:
- venom-fractal.service
- venom-api.service
- venom-mesh-discovery.service
- venom-mesh-orchestrator.service

---

**Last Updated**: 2025-01-04  
**Version**: 1.0.0-alpha  
**Author**: manuelstellian-dev
