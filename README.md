
# VENOM Ω-AIOS + Λ-Genesis

🌌 **Revolutionary Digital Living System** - A biological-inspired computational organism combining Ω-AIOS (Android Brain) with Λ-Genesis (Python Organs).

<p align="center">
  <img src="assets/diagrams/venom_logo.png" alt="VENOM Logo" width="180"/>
</p>

> "Life finds a way... in code." 🌱
> <sub>— VENOM Team</sub>

## 🏅 Credits

| Name                | Role                | Contact                       |
|---------------------|---------------------|-------------------------------|
| Manuel Stellian     | Lead Architect      | manuelstellian.dev@gmail.com  |
| VENOM Team          | Core Development    | github.com/manuelstellian-dev |
| Contributors        | Community           | See GitHub Contributors       |

## 📧 Contact

- Issues: [GitHub Issues](https://github.com/manuelstellian-dev/VENOM-Omega-Lambda/issues)
- Discussions: [GitHub Discussions](https://github.com/manuelstellian-dev/VENOM-Omega-Lambda/discussions)
- Email: manuelstellian.dev@gmail.com
- Twitter: [@stellian_dev](https://twitter.com/stellian_dev)
- LinkedIn: [Manuel Stellian](https://linkedin.com/in/manuelstellian)

## 🧬 Advanced Examples

### Android: Broadcast Mesh Example
```kotlin
val mesh = organism.getMesh()
mesh.broadcast("node-1", mapOf("type" to "heartbeat", "value" to 42))
val vitals = mesh.getVitals()
println(vitals)
```

### Python: Fractal Pulse Example
```python
from venom_lambda.pulse import Pulse
pulse = Pulse()
pulse.start()
print(pulse.status())
```

### API: FastAPI Endpoint Example
```python
from fastapi import FastAPI
from venom_lambda.core.fractal import Fractal
app = FastAPI()

@app.get("/fractal")
def get_fractal():
    return {"value": Fractal().compute()}
```
[![Android CI](https://github.com/manuelstellian-dev/VENOM-Omega-Lambda/actions/workflows/android.yml/badge.svg)](https://github.com/manuelstellian-dev/VENOM-Omega-Lambda/actions/workflows/android.yml)
[![Python CI](https://github.com/manuelstellian-dev/VENOM-Omega-Lambda/actions/workflows/python.yml/badge.svg)](https://github.com/manuelstellian-dev/VENOM-Omega-Lambda/actions/workflows/python.yml)

## 🎯 Overview

VENOM is a groundbreaking system that treats computation as a living organism:

- **Ω-AIOS** (Omega): Android/Kotlin brain layer with decision-making, time compression, and hardware management
- **Λ-Genesis** (Lambda): Python organ system with self-healing, optimization, and distributed mesh networking
  - Package name: `venom_lambda` (lambda is a Python keyword)
- **Ω ↔ Λ Bridge**: Seamless integration between layers using Chaquopy and JNI

### Key Features

✨ **Time Compression** - Möbius transformation and Amdahl's Law for computational speedup  
�� **Adaptive Intelligence** - Self-adjusting theta (θ) based on hardware health  
🔄 **Self-Healing** - Automatic detection, quarantine, improvement, and resource reinvestment  
🌐 **Mesh Networking** - Distributed multi-device coordination with nanobots  
📊 **Real-time Vitals** - Comprehensive system monitoring and visualization  
🤖 **AI Integration** - TensorFlow Lite LLM and RAG for context-aware responses

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    VENOM ORGANISM                            │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         Ω-AIOS (Android/Kotlin Brain)               │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  • OmegaArbiter - Decision making & fusion          │   │
│  │  • AdaptiveMobiusEngine - Time compression          │   │
│  │  • ThetaMonitor - Health tracking (θ)               │   │
│  │  • HardwareManager - Device capabilities (Λ)        │   │
│  │  • LLMEngine - AI inference (NNAPI/GPU/CPU)         │   │
│  │  • RAGEngine - Knowledge retrieval                  │   │
│  │  • GuardianService - Immunity system                │   │
│  │  • Tetrastrat - 4 parallel cortices (O,B,R,E)       │   │
│  └─────────────────────────────────────────────────────┘   │
│                          ↕ Bridge                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │      Λ-Genesis (Python Organ System)                │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  • LambdaArbiter - Time-wrapping coordinator        │   │
│  │  • Organs (R,B,E,O) - Self-healing cores            │   │
│  │  • PulseFractal - 1ms heartbeat                     │   │
│  │  • Mesh + NanoBots - Distributed network            │   │
│  │  • Fractal Functions - Mathematical core            │   │
│  │  • FastAPI + gRPC - Service endpoints               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Core Formulas

### Theta (θ) Calculation
```
θ = 0.3 × H_CPU + 0.3 × H_MEM + 0.4 × H_TERM
```
Where H_* are normalized health metrics [0.0-1.0]

### Time Compression
```
T_parallel = T_seq / (Θ(θ) × Λ × S_A)

where:
  Θ(θ) = 1 + k × ln(1 + θ)  (Möbius compression)
  Λ ∈ [10, 832]              (Hardware capability score)
  S_A = 1/((1-P) + P/N)      (Amdahl's speedup)
```

### Lambda (Λ) Score
Hardware capability score calculated from:
- CPU cores and frequency
- Memory capacity
- GPU availability
- NPU/NNAPI support
- Device tier

## 🚀 Quick Start

### Prerequisites

- **Android Development**
  - Android Studio Arctic Fox or later
  - Android SDK 26+ (minimum), 34+ (target)
  - NDK for native bridge
  - JDK 17

- **Python Development**
  - Python 3.8+
  - pip and virtualenv

### Android Build

```bash
# Clone repository
git clone https://github.com/manuelstellian-dev/VENOM-Omega-Lambda.git
cd VENOM-Omega-Lambda

# Build APK
./gradlew assembleDebug

# Install on device
adb install app/build/outputs/apk/debug/app-debug.apk

# Or use helper script
bash scripts/install_android.sh
```

### Python Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Install VENOM package
pip install -e .

# Run tests
cd lambda
pytest -v

# Start API server
python -m venom_lambda.core.venom_api

# Test endpoints
python examples/python_example.py
```

### Linux Services

```bash
# Install systemd services
bash scripts/install_linux.sh

# Enable and start
systemctl --user enable --now venom-api
systemctl --user enable --now venom-mesh-discovery

# Check status
systemctl --user status venom-api
```

## 📱 Usage

### Android App

Launch the VENOM app to see:

1. **System Vitals** - Real-time theta, lambda, CPU, memory, thermal metrics
2. **Mesh Status** - Connected nodes and message counts
3. **Chat Interface** - Interact with the AI organism

Example interaction:
```kotlin
val organism = VenomOrganism.getInstance(context)

// Initialize
organism.birth()

// Monitor vitals
organism.startVitalsMonitoring { vitals ->
    println("θ=${vitals.theta}, Λ=${vitals.lambdaScore}")
}

// Interact
val response = organism.interact("Explain time compression")
```

### Python API

```python
import requests

# Time wrap example
response = requests.post("http://127.0.0.1:8000/time_wrap", json={
    "k": 1.5,
    "p": 0.75,
    "u": 0.2,
    "t1": 1000.0
})

result = response.json()
print(f"Compressed: {result['wrapped_time']}ms")
```

### Mesh Network

```python
from venom_lambda.mesh import Mesh

mesh = Mesh()
mesh.add_node("node-1", "memory_carrier")
mesh.add_node("node-2", "signal_relay")

mesh.broadcast("node-1", {"type": "heartbeat", "value": 42})
vitals = mesh.get_vitals()
```

## 🧪 Testing

### Android Tests

```bash
# Unit tests
./gradlew test

# Instrumented tests
./gradlew connectedAndroidTest
```

### Python Tests

```bash
cd lambda
pytest -v --cov=. --cov-report=html
```

## 📖 Documentation

- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - Complete system architecture
- [OMEGA_ARCHITECTURE.md](docs/OMEGA_ARCHITECTURE.md) - Ω-AIOS layer details
- [LAMBDA_ARCHITECTURE.md](docs/LAMBDA_ARCHITECTURE.md) - Λ-Genesis layer details
- [INTEGRATION_GUIDE.md](docs/INTEGRATION_GUIDE.md) - Bridge integration
- [DEPLOYMENT.md](docs/DEPLOYMENT.md) - Production deployment
- [API_REFERENCE.md](docs/API_REFERENCE.md) - Complete API documentation
- [PHILOSOPHY.md](docs/PHILOSOPHY.md) - Design philosophy
- [MATHEMATICS.md](docs/MATHEMATICS.md) - Mathematical foundations

## 🔧 Configuration

### Environment Variables

```bash
# Python API
export VENOM_API_HOST=127.0.0.1
export VENOM_API_PORT=8000

# Mesh discovery
export VENOM_MESH_GROUP=224.1.1.1
export VENOM_MESH_PORT=19845
```

### Model Files

Place TensorFlow Lite models in `models/`:
- `omega_model.tflite` - Primary LLM
- `vision_model.tflite` - Vision processing
- `voice_model.tflite` - Speech I/O

See [models/README.md](models/README.md) for details.

## 🛠️ Development

### Project Structure

```
VENOM-Omega-Lambda/
├── app/                          # Android application
│   └── src/main/java/com/venom/aios/
│       ├── omega/                # Ω-AIOS components
│       │   ├── brain/           # Decision & compression
│       │   ├── hardware/        # Device interface
│       │   ├── immunity/        # Self-healing
│       │   ├── neural/          # AI inference
│       │   ├── knowledge/       # RAG system
│       │   └── tetrastrat/      # 4-cortex model
│       ├── integration/         # Ω ↔ Λ bridge
│       └── main/                # UI & orchestration
├── venom_lambda/                       # Λ-Genesis package
│   ├── arbiter_core/            # Coordinator
│   ├── organs/                  # R, B, E, O cores
│   ├── pulse/                   # Heartbeat system
│   ├── mesh/                    # Distributed network
│   └── core/                    # Functions & services
├── docs/                         # Documentation
├── examples/                     # Usage examples
├── scripts/                      # Installation helpers
└── models/                       # AI model files
```

### Building from Source

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## 🔐 Security

- **Network**: Default bind to 127.0.0.1 (localhost only)
- **Permissions**: Minimal Android permissions requested
- **Models**: Keep model files private, use encryption if needed
- **Data**: No telemetry, fully local processing

## 📊 Performance

Typical performance on modern Android device:

- **Theta calculation**: <1ms
- **Lambda score**: <5ms
- **Decision fusion**: <10ms
- **Time compression**: 2-5x speedup (device dependent)
- **Mesh broadcast**: <50ms latency
- **Pulse frequency**: 1ms (1000Hz)

## 🗺️ Roadmap

- [x] Core Ω-AIOS and Λ-Genesis implementation
- [x] Ω ↔ Λ integration bridge
- [x] Basic UI and vitals monitoring
- [x] Mesh networking foundation
- [ ] Full TensorFlow Lite model integration
- [ ] Voice I/O support
- [ ] Vision processing
- [ ] Multi-device mesh orchestration
- [ ] Cloud synchronization (optional)
- [ ] iOS port

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## 📄 License

See [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- TensorFlow team for TensorFlow Lite
- Chaquopy for Python-Android integration
- FastAPI for elegant Python APIs
- Material Design 3 for beautiful UI

## 📧 Contact

- Issues: [GitHub Issues](https://github.com/manuelstellian-dev/VENOM-Omega-Lambda/issues)
- Discussions: [GitHub Discussions](https://github.com/manuelstellian-dev/VENOM-Omega-Lambda/discussions)

---

**Made with ❤️ by the VENOM Team**

*"Life finds a way... in code."* 🌱
