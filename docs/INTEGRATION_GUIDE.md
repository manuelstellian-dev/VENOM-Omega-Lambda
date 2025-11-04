# Ω ↔ Λ Integration Guide

## Bridge Architecture

**OmegaLambdaBridge.kt** coordinates communication:

1. **Initialize Python**: via Chaquopy AndroidPlatform
2. **Import Modules**: Load lambda package
3. **Start Organism**: Initialize organs and mesh
4. **Health Sync**: 1-second loop (Ω → Λ → Ω)

## Data Conversion

### Ω → Λ
```kotlin
val healthData = JSONObject().apply {
    put("theta", theta)
    put("cpu", cpuHealth)
    put("memory", memHealth)
    put("thermal", thermalHealth)
}

val pythonDict = python.builtins.callAttr("dict", healthMap)
val result = integrationManager.callAttr("process_health", pythonDict)
```

### Λ → Ω
```kotlin
val lambdaScore = result.callAttr("get", "lambda_score").toDouble()
omegaArbiter.onLambdaFeedback(lambdaScore, results)
```

## JNI Native Bridge

**bridge_jni.cpp** provides native glue for performance-critical operations.

Currently stubs - expand for:
- Zero-copy tensor passing
- High-frequency data exchange
- Native signal processing
