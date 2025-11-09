# Integration Guide - Ω ↔ Λ

**How Omega and Lambda Communicate**

---

## Table of Contents

1. [Overview](#overview)
2. [Bridge Architecture](#bridge-architecture)
3. [Communication Flow](#communication-flow)
4. [Data Formats](#data-formats)
5. [Performance Optimization](#performance-optimization)
6. [Troubleshooting](#troubleshooting)

---

## Overview

The **Integration Bridge** connects two fundamentally different layers:

- **Ω-AIOS**: Kotlin/Android (JVM)
- **Λ-GENESIS**: Python (CPython)

This is achieved through:
1. **Chaquopy** - Python runtime in Android process
2. **JNI** - Native bridge for performance-critical operations
3. **JSON** - Data serialization format

---

## Bridge Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Android Process                       │
│                                                           │
│  ┌──────────────────┐                                    │
│  │  Kotlin (JVM)    │                                    │
│  │  ===============  │                                    │
│  │  VenomOrganism   │                                    │
│  │  OmegaArbiter    │                                    │
│  │  ThetaMonitor    │                                    │
│  └────────┬─────────┘                                    │
│           │                                               │
│           ↓                                               │
│  ┌──────────────────────────────────────────────┐       │
│  │  OmegaLambdaBridge (Kotlin)                  │       │
│  │  =========================================    │       │
│  │  • Health data collection                    │       │
│  │  • JSON serialization                        │       │
│  │  • Python module imports (Chaquopy)          │       │
│  │  • Result processing                         │       │
│  └────────┬─────────────────────────────────────┘       │
│           │                                               │
│           ↓                                               │
│  ┌──────────────────────────────────────────────┐       │
│  │  Chaquopy Bridge                             │       │
│  │  =========================================    │       │
│  │  • Python interpreter in JVM                 │       │
│  │  • Module loading                            │       │
│  │  • Type conversion (Kotlin ↔ Python)        │       │
│  └────────┬─────────────────────────────────────┘       │
│           │                                               │
│           ↓                                               │
│  ┌──────────────────┐                                    │
│  │  Python (CPython)│                                    │
│  │  ===============  │                                    │
│  │  LambdaArbiter   │                                    │
│  │  4 Organs        │                                    │
│  │  PulseFractal    │                                    │
│  │  Mesh            │                                    │
│  └──────────────────┘                                    │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

## Bridge Architecture

### **OmegaLambdaBridge.kt**

**Location**: `integration/OmegaLambdaBridge.kt`

#### Initialization

```kotlin
class OmegaLambdaBridge(
    private val context: Context,
    private val omegaArbiter: OmegaArbiter,
    private val thetaMonitor: ThetaMonitor,
    private val hardwareManager: HardwareManager
) {
    init {
        initializePython()
    }
}
```

#### Python Runtime Setup

```kotlin
private fun initializePython() {
    // Initialize Chaquopy
    if (!Python.isStarted()) {
        Python.start(AndroidPlatform(context))
        Log.i(TAG, "✅ Python runtime initialized")
    }
    
    python = Python.getInstance()
    importLambdaModules()
}
```

#### Module Imports

```kotlin
private fun importLambdaModules() {
    val py = python ?: return
    
    // Import Lambda Arbiter
    val arbiterModule = py.getModule("lambda.arbiter_core.arbiter")
    val arbiterClass = arbiterModule["LambdaArbiter"]
    lambdaArbiter = arbiterClass?.call()
    
    // Import Pulse
    val pulseModule = py.getModule("lambda.pulse.pulse")
    val pulseClass = pulseModule["PulseFractal"]
    lambdaPulse = pulseClass?.call(lambdaArbiter)
    
    // Import Mesh
    val meshModule = py.getModule("lambda.mesh.mesh")
    val meshClass = meshModule["Mesh"]
    lambdaMesh = meshClass?.call()
    
    Log.i(TAG, "✅ Lambda modules imported")
}
```

---

## Communication Flow

### **1. Health Sync Loop (1s interval)**

```kotlin
private fun startHealthSync() {
    scope.launch {
        while (bridgeActive) {
            try {
                // 1. Collect Omega health
                val omegaHealth = collectOmegaHealth()
                
                // 2. Send to Lambda
                val lambdaResults = executeLambdaTimeWrap(omegaHealth)
                
                // 3. Process results
                processLambdaResults(lambdaResults)
                
                delay(HEALTH_SYNC_INTERVAL) // 1000ms
                
            } catch (e: Exception) {
                Log.e(TAG, "Health sync error: ${e.message}")
            }
        }
    }
}
```

### **2. Collect Omega Health**

```kotlin
private fun collectOmegaHealth(): JSONObject {
    val memInfo = hardwareManager.getMemoryInfo()
    val thermalInfo = hardwareManager.getThermalInfo()
    val batteryInfo = hardwareManager.getBatteryInfo()
    val cpuInfo = hardwareManager.getCPUInfo()
    val theta = thetaMonitor.currentTheta
    
    return JSONObject().apply {
        put("theta", theta)
        put("cpu_health", getCPUHealth())
        put("memory_health", 1.0 - (memInfo.usedRAM.toDouble() / memInfo.totalRAM))
        put("thermal_health", thermalInfo.health)
        put("battery_level", batteryInfo.level)
        put("model_corruption", false)
        put("cache_size", getCacheSize())
        put("cpu_cores", cpuInfo.cores)
    }
}
```

**Example Output**:
```json
{
  "theta": 0.75,
  "cpu_health": 0.8,
  "memory_health": 0.85,
  "thermal_health": 0.9,
  "battery_level": 80,
  "model_corruption": false,
  "cache_size": 50000000,
  "cpu_cores": 8
}
```

### **3. Execute Lambda TimeWrap**

```kotlin
private fun executeLambdaTimeWrap(healthData: JSONObject): JSONObject {
    val py = python ?: return JSONObject().apply { 
        put("error", "Python not initialized") 
    }
    
    // Convert JSONObject to Python dict
    val pyDict = py.getBuiltins()?.callAttr("dict")
    healthData.keys().forEach { key =>
        pyDict?.put(key, healthData.get(key))
    }
    
    // Execute Lambda time_wrap
    val result = lambdaArbiter?.callAttr("time_wrap", pyDict)
    
    // Convert result back to JSON
    val resultJson = JSONObject()
    resultJson.put("integrated_score", result?.get("integrated_score")?.toDouble() ?: 0.0)
    resultJson.put("organs", result?.get("organs")?.toString() ?: "{}")
    
    return resultJson
}
```

### **4. Process Lambda Results**

```kotlin
private fun processLambdaResults(results: JSONObject) {
    val integratedScore = results.optDouble("integrated_score", 0.0)
    
    // Feed back to Omega Arbiter
    omegaArbiter.onLambdaFeedback(integratedScore, results)
    
    // Broadcast to mesh
    lambdaMesh?.callAttr(
        "broadcast",
        "omega_bridge",
        "Omega health sync: score=${"%.3f".format(integratedScore)}"
    )
    
    Log.d(TAG, "✅ Lambda feedback: ${"%.3f".format(integratedScore)}")
}
```

---

## Data Formats

### **Health Data (Ω → Λ)**

**Type**: `JSONObject` (Kotlin) → `Dict[str, Any]` (Python)

**Schema**:
```typescript
{
  theta: number,              // 0.0 - 1.0
  cpu_health: number,         // 0.0 - 1.0
  memory_health: number,      // 0.0 - 1.0
  thermal_health: number,     // 0.0 - 1.0
  battery_level: number,      // 0 - 100
  model_corruption: boolean,
  cache_size: number,         // bytes
  cpu_cores: number
}
```

### **Lambda Results (Λ → Ω)**

**Type**: `Dict[str, Any]` (Python) → `JSONObject` (Kotlin)

**Schema**:
```typescript
{
  organs: {
    REGEN: {
      organ: "REGEN",
      action: "monitoring" | "regenerating",
      issues: number,
      repaired: number
    },
    BALANCE: {
      organ: "BALANCE",
      action: "balancing",
      stability: string,
      theta: number
    },
    ENTROPY: {
      organ: "ENTROPY",
      action: "defending",
      threats_detected: number,
      defended: number
    },
    OPTIMIZE: {
      organ: "OPTIMIZE",
      action: "optimizing",
      targets: number,
      adjustments: string[]
    }
  },
  integrated_score: number,    // 0.0 - 1.0
  genome_balance: {
    R: number,
    B: number,
    E: number,
    O: number,
    Λ: number
  },
  timestamp: string
}
```

---

## Performance Optimization

### **1. JNI Bridge (Optional)**

**Location**: `integration/bridge_jni.cpp`

For performance-critical operations, use JNI:

```cpp
// Fast JSON serialization
JNIEXPORT jstring JNICALL
Java_com_venom_integration_OmegaLambdaBridge_serializeHealthData(
    JNIEnv* env,
    jobject obj,
    jdouble theta,
    jdouble cpuHealth,
    jdouble memoryHealth,
    jdouble thermalHealth) {
    
    char buffer[512];
    snprintf(buffer, sizeof(buffer),
        "{\"theta\":%.3f,\"cpu_health\":%.3f,\"memory_health\":%.3f,\"thermal_health\":%.3f}",
        theta, cpuHealth, memoryHealth, thermalHealth);
    
    return env->NewStringUTF(buffer);
}
```

**Usage**:
```kotlin
external fun serializeHealthData(
    theta: Double,
    cpuHealth: Double,
    memoryHealth: Double,
    thermalHealth: Double
): String
```

**Performance Gain**: ~2-3× faster than Kotlin JSON serialization

### **2. Batch Operations**

Instead of calling Python for each operation:

```kotlin
// ❌ Bad: Multiple calls
lambdaArbiter?.callAttr("some_function")
lambdaArbiter?.callAttr("another_function")
lambdaArbiter?.callAttr("third_function")

// ✅ Good: Single batched call
val operations = listOf("op1", "op2", "op3")
lambdaArbiter?.callAttr("batch_execute", operations)
```

### **3. Async Execution**

Use Kotlin coroutines for non-blocking calls:

```kotlin
suspend fun executeLambdaAsync(data: JSONObject): JSONObject = 
    withContext(Dispatchers.Default) {
        executeLambdaTimeWrap(data)
    }
```

---

## Troubleshooting

### **Issue 1: Python not initialized**

**Error**: `Python.isStarted() returns false`

**Solution**:
```kotlin
// Ensure Python.start() is called before any Python operations
if (!Python.isStarted()) {
    Python.start(AndroidPlatform(context))
}
```

### **Issue 2: Module import fails**

**Error**: `ModuleNotFoundError: No module named 'lambda'`

**Solution**:
```kotlin
// Check Chaquopy configuration in build.gradle.kts
chaquopy {
    defaultConfig {
        pip {
            install("fastapi")
            install("uvicorn")
            // ... other dependencies
        }
    }
    
    sourceSets {
        getByName("main") {
            srcDir("src/main/python")
        }
    }
}
```

### **Issue 3: Type conversion errors**

**Error**: `Cannot convert Python object to Kotlin type`

**Solution**:
```kotlin
// Use safe type conversion
val result = pythonObject?.get("key")
val value = when {
    result == null -> defaultValue
    result is PyObject -> result.toDouble()
    else -> defaultValue
}
```

### **Issue 4: Memory leaks**

**Error**: Python objects not released

**Solution**:
```kotlin
// Explicitly close Python objects
try {
    val result = lambdaArbiter?.callAttr("time_wrap", data)
    // Process result
} finally {
    // Chaquopy handles cleanup automatically
    // But you can force GC if needed
    System.gc()
}
```

### **Issue 5: Slow performance**

**Symptoms**: Health sync takes >100ms

**Solutions**:
1. Use JNI for serialization (see above)
2. Reduce health sync frequency
3. Cache Python module references
4. Use batch operations

```kotlin
// Cache module references
private var cachedArbiter: PyObject? = null

private fun getCachedArbiter(): PyObject? {
    if (cachedArbiter == null) {
        cachedArbiter = lambdaArbiter
    }
    return cachedArbiter
}
```

---

## Testing Integration

### **Unit Test (Kotlin)**

```kotlin
@Test
fun testBridgeHealthSync() = runBlocking {
    val bridge = OmegaLambdaBridge(context, arbiter, theta, hardware)
    
    val health = bridge.collectOmegaHealth()
    assertNotNull(health)
    
    val results = bridge.executeLambdaTimeWrap(health)
    assertTrue(results.has("integrated_score"))
}
```

### **Integration Test (Python)**

```python
def test_integration_manager():
    manager = IntegrationManager()
    assert manager.initialize_lambda()
    
    health_data = {
        "theta": 0.75,
        "cpu_health": 0.8
    }
    
    results = manager.process_health_data(health_data)
    assert "integrated_score" in results
    assert 0.0 <= results["integrated_score"] <= 1.0
```

---

## Best Practices

### **1. Error Handling**

Always wrap Python calls in try-catch:

```kotlin
try {
    val result = lambdaArbiter?.callAttr("time_wrap", data)
} catch (e: PyException) {
    Log.e(TAG, "Python error: ${e.message}")
    // Return fallback result
} catch (e: Exception) {
    Log.e(TAG, "Bridge error: ${e.message}")
}
```

### **2. Timeout Protection**

Use timeouts for Python operations:

```kotlin
withTimeout(5000) {  // 5 seconds
    executeLambdaTimeWrap(data)
}
```

### **3. State Synchronization**

Keep Omega and Lambda states in sync:

```kotlin
// After successful Lambda execution
omegaArbiter.onLambdaFeedback(score, results)
thetaMonitor.updateFromLambda(score)
```

### **4. Logging**

Log all bridge operations for debugging:

```kotlin
Log.d(TAG, "→ Sending to Lambda: $healthData")
val result = executeLambdaTimeWrap(healthData)
Log.d(TAG, "← Received from Lambda: $result")
```

---

## Advanced Topics

### **Multi-Threading**

Bridge operations are thread-safe:

```kotlin
// Multiple threads can call bridge simultaneously
scope.launch(Dispatchers.IO) {
    bridge.executeLambdaTimeWrap(data1)
}

scope.launch(Dispatchers.Default) {
    bridge.executeLambdaTimeWrap(data2)
}
```

### **Custom Python Functions**

Add custom functions to Lambda layer:

**Python (lambda/custom/my_function.py)**:
```python
def my_custom_function(data):
    # Custom processing
    return {"result": "custom"}
```

**Kotlin**:
```kotlin
val customModule = python?.getModule("lambda.custom.my_function")
val customFunc = customModule?.get("my_custom_function")
val result = customFunc?.call(data)
```

---

**Last Updated**: 2025-01-04  
**Version**: 1.0.0-alpha  
**Author**: manuelstellian-dev
