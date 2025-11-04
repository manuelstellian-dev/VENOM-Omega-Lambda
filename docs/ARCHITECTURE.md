# VENOM System Architecture

## Overview

VENOM is a dual-layer biological-inspired computational system:

- **Ω-AIOS**: Android/Kotlin brain layer (decision-making, hardware interfacing)
- **Λ-Genesis**: Python organ system (self-healing, distributed processing)

## Layer Communication

```
┌─────────────┐    Health Data     ┌─────────────┐
│   Ω-AIOS    │ ───────────────→   │  Λ-Genesis  │
│   (Brain)   │                     │  (Organs)   │
│             │ ←───────────────   │             │
└─────────────┘   Lambda Feedback  └─────────────┘
     Bridge: Chaquopy + JNI + Integration Manager
```

### Data Flow

1. **Ω → Λ**: ThetaMonitor collects health (θ, CPU, MEM, TERM)
2. **Bridge**: OmegaLambdaBridge converts JSON ↔ Python dict
3. **Λ Processing**: LambdaArbiter applies time-wrapping, organs process
4. **Λ → Ω**: Lambda score (Λ) and adjustments returned
5. **Ω Recalibration**: OmegaArbiter adjusts theta based on feedback

## Components

### Ω-AIOS Components

- **OmegaArbiter**: Master decision maker
- **AdaptiveMobiusEngine**: Time compression (Möbius + Amdahl)
- **ThetaMonitor**: Real-time health monitoring
- **HardwareManager**: Device capability assessment
- **LLMEngine**: AI inference engine
- **RAGEngine**: Knowledge retrieval
- **GuardianService**: Immunity and self-healing
- **Tetrastrat**: 4-cortex parallel processing

### Λ-Genesis Components

- **LambdaArbiter**: Time-wrapping coordinator
- **Organs (R,B,E,O)**: Self-healing, balancing, entropy, optimization
- **PulseFractal**: 1ms heartbeat synchronization
- **Mesh + NanoBots**: Distributed network
- **Services**: FastAPI REST + gRPC + mesh discovery/orchestration

## State Management

### Ω State
- Current theta (θ)
- Lambda score (Λ)
- Hardware metrics
- AI model status

### Λ State
- Genome configuration
- Organ vitals
- Mesh topology
- Pulse beat count

## Scalability

- **Single Device**: Ω + Λ co-located
- **Multi-Device**: Mesh networking for distributed Λ organs
- **Cloud**: Optional remote Λ deployment
