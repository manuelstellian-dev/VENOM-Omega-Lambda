# Ω-AIOS Architecture

## Brain Layer (Android/Kotlin)

### Core Components

#### 1. OmegaArbiter
- **Purpose**: Master decision maker
- **Methods**:
  - `makeDecision()`: Process user input with context
  - `fuseDecisions()`: Merge user intent + AI suggestion
  - `onLambdaFeedback()`: Adjust from Λ feedback
  - `executeWithCompression()`: Apply theta compression

#### 2. AdaptiveMobiusEngine
- **Purpose**: Time compression and speedup calculation
- **Formulas**:
  - `θ = 0.3×H_CPU + 0.3×H_MEM + 0.4×H_TERM`
  - `Θ(θ) = 1 + k×ln(1+θ)` (Möbius)
  - `S_A = 1/((1-P) + P/N)` (Amdahl)
  - `T_parallel = T_seq / (Θ(θ) × Λ × S_A)`

#### 3. ThetaMonitor
- **Purpose**: Continuous health monitoring
- **Metrics**: CPU, memory, thermal health
- **Frequency**: 1 second updates
- **Callbacks**: Subscribe to theta changes

#### 4. HardwareManager
- **Purpose**: Device capability assessment
- **Calculates**: Lambda (Λ) score [10-832]
- **Factors**: Cores, memory, GPU, NPU, device tier

#### 5. LLMEngine
- **Purpose**: On-device AI inference
- **Modes**: LITE (quantized), BALANCED, FULL
- **Fallback**: NNAPI → GPU → CPU

#### 6. RAGEngine
- **Purpose**: Retrieval-Augmented Generation
- **Sources**: Wikipedia, papers, code repos
- **Search**: Vector similarity (FAISS stub)

#### 7. GuardianService
- **Purpose**: Self-healing immunity system
- **Cycle**: DETECT → QUARANTINE → IMPROVE → REINVEST
- **Threats**: Low memory, high CPU, thermal, storage

#### 8. Tetrastrat Engines
- **OptimizeEngine**: Performance optimization
- **BalanceEngine**: Resource balancing
- **RegenerateEngine**: Self-healing
- **EntropyEngine**: Chaos testing and defense

## Integration

OmegaLambdaBridge coordinates all components and manages Ω ↔ Λ communication.
