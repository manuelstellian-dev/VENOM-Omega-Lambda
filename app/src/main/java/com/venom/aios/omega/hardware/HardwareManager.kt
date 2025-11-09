package com.venom.aios.omega.hardware

import android.app.ActivityManager
import android.content.Context
import android.os.Build
import android.util.Log
import org.json.JSONObject
import java.io.File
import android.opengl.EGL14
import android.opengl.GLES20
import android.os.BatteryManager
import androidx.core.content.getSystemService
import android.hardware.Sensor
import android.hardware.SensorManager
import org.json.JSONArray

/**
 * HardwareManager - Interface to device hardware capabilities
 * 
 * Calculates Lambda (Λ) score based on hardware capabilities:
 * Λ ∈ [10, 832] where higher is better
 */
class HardwareManager(private val context: Context) {
    private val TAG = "HardwareManager"
    
    /**
     * Get CPU information
     * @return JSON object with CPU details
     */
    fun getCPUInfo(): JSONObject {
        val cpuInfo = JSONObject()
        try {
            val typed = getCPUInfoTyped()
            val cpuAbi = Build.SUPPORTED_ABIS.joinToString(", ")

            cpuInfo.put("cores", typed.cores)
            cpuInfo.put("abi", cpuAbi)
            cpuInfo.put("architecture", typed.architecture)

            // expose MHz for backward compatibility (typed stores kHz)
            if (typed.maxFrequencyKHz > 0) {
                cpuInfo.put("maxFrequencyMHz", typed.maxFrequencyKHz / 1000)
            }

            // Also expose kHz explicitly so callers can choose units unambiguously
            if (typed.maxFrequencyKHz > 0) {
                cpuInfo.put("maxFrequencyKHz", typed.maxFrequencyKHz)
            }

            Log.d(TAG, "CPU Info (typed): ${typed.cores} cores, $cpuAbi")
        } catch (e: Exception) {
            Log.e(TAG, "Error reading CPU info", e)
        }
        return cpuInfo
    }
    
    /**
     * Get GPU information
     * @return JSON object with GPU details
     */
    fun getGPUInfo(): JSONObject {
        val gpuInfo = JSONObject()
        try {
            val typed = getGPUInfoTyped()
            gpuInfo.put("renderer", typed.renderer)
            gpuInfo.put("vendor", typed.vendor)
            gpuInfo.put("version", typed.version)
            gpuInfo.put("available", !(typed.renderer == "Unknown" && typed.vendor == "Unknown"))
            Log.d(TAG, "GPU Info (typed): ${typed.renderer}")
        } catch (e: Exception) {
            Log.e(TAG, "Error reading GPU info", e)
        }
        return gpuInfo
    }
    
    /**
     * Get NPU information
     * @return JSON object with NPU details
     */
    fun getNPUInfo(): JSONObject {
        val npuInfo = JSONObject()
        try {
            val typed = getNPUInfoTyped()
            npuInfo.put("nnapi_available", typed.available)
            npuInfo.put("type", typed.type)
            npuInfo.put("chipset", typed.chipset)
            Log.d(TAG, "NPU Info (typed): ${typed.type} available=${typed.available}")
        } catch (e: Exception) {
            Log.e(TAG, "Error reading NPU info", e)
        }
        return npuInfo
    }
    
    /**
     * Get memory information
     * @return JSON object with memory details
     */
    fun getMemoryInfo(): JSONObject {
        val memInfo = JSONObject()
        try {
            val typed = getMemoryInfoTyped()
            val totalMB = typed.totalRAM / (1024 * 1024)
            val availMB = typed.availableRAM / (1024 * 1024)
            val usedMB = typed.usedRAM / (1024 * 1024)

            memInfo.put("totalMB", totalMB)
            memInfo.put("availableMB", availMB)
            memInfo.put("usedMB", usedMB)
            memInfo.put("lowMemory", typed.lowMemory)
            memInfo.put("threshold", typed.threshold / (1024 * 1024))

            Log.d(TAG, "Memory (typed): ${usedMB}/${totalMB} MB used")
        } catch (e: Exception) {
            Log.e(TAG, "Error reading memory info", e)
        }
        return memInfo
    }
    
    /**
     * Get thermal information
     * @return JSON object with thermal details
     */
    fun getThermalInfo(): JSONObject {
        val thermalInfo = JSONObject()
        try {
            val typed = getThermalInfoTyped()
            thermalInfo.put("temperatureCelsius", typed.temperature)
            thermalInfo.put("health", typed.health)
            thermalInfo.put("throttling", typed.throttling.name)
            Log.d(TAG, "Thermal Info (typed): temp=${typed.temperature}C health=${typed.health}")
        } catch (e: Exception) {
            Log.e(TAG, "Error reading thermal info", e)
        }
        return thermalInfo
    }
    
    /**
     * Get battery information
     * @return JSON object with battery details
     */
    fun getBatteryInfo(): JSONObject {
        val batteryInfo = JSONObject()
        try {
            val typed = getBatteryInfoTyped()
            batteryInfo.put("level", typed.level)
            batteryInfo.put("charging", typed.isCharging)
            batteryInfo.put("temperatureCelsius", typed.temperature)
            Log.d(TAG, "Battery Info (typed): level=${typed.level}% charging=${typed.isCharging}")
        } catch (e: Exception) {
            Log.e(TAG, "Error reading battery info", e)
        }
        return batteryInfo
    }
    
    /**
     * Get all available sensors
     * @return JSON array of sensor information
     */
    fun getAllSensors(): JSONObject {
        val sensors = JSONObject()
        try {
            val typed = getAllSensorsTyped()
            val arr = JSONArray()
            for (s in typed) {
                val o = JSONObject()
                o.put("name", s.name)
                o.put("type", s.type)
                o.put("vendor", s.vendor)
                arr.put(o)
            }
            sensors.put("sensors", arr)
            Log.d(TAG, "Sensors enumerated: count=${typed.size}")
        } catch (e: Exception) {
            Log.e(TAG, "Error reading sensors", e)
        }

        return sensors
    }

    /* Legacy (non-destructive) implementations
       Kept for compatibility: original implementations are preserved
       under "Legacy" names so callers can opt-in if they relied on
       the previous behavior. These do not remove the new typed APIs. */

    fun getCPUInfoLegacy(): JSONObject {
        val cpuInfo = JSONObject()
        try {
            val nCores = Runtime.getRuntime().availableProcessors()
            val cpuAbi = Build.SUPPORTED_ABIS.joinToString(", ")

            cpuInfo.put("cores", nCores)
            cpuInfo.put("abi", cpuAbi)
            cpuInfo.put("architecture", System.getProperty("os.arch") ?: "unknown")

            // Read CPU frequency if available (legacy returned MHz)
            val maxFreq = readCPUMaxFrequency()
            if (maxFreq > 0) {
                cpuInfo.put("maxFrequencyMHz", maxFreq)
            }

            Log.d(TAG, "CPU Info (legacy): $nCores cores, $cpuAbi")
        } catch (e: Exception) {
            Log.e(TAG, "Error reading CPU info (legacy)", e)
        }
        return cpuInfo
    }

    fun getGPUInfoLegacy(): JSONObject {
        val gpuInfo = JSONObject()
        try {
            // Legacy implementation used placeholders; keep same behavior here
            gpuInfo.put("renderer", "unknown")
            gpuInfo.put("vendor", "unknown")
            gpuInfo.put("available", hasGPULegacy())

            Log.d(TAG, "GPU available (legacy): ${hasGPULegacy()}")
        } catch (e: Exception) {
            Log.e(TAG, "Error reading GPU info (legacy)", e)
        }
        return gpuInfo
    }

    fun getNPUInfoLegacy(): JSONObject {
        val npuInfo = JSONObject()
        try {
            val hasNNAPI = Build.VERSION.SDK_INT >= Build.VERSION_CODES.O_MR1
            npuInfo.put("nnapi_available", hasNNAPI)
            npuInfo.put("nnapi_version", if (hasNNAPI) Build.VERSION.SDK_INT else 0)

            Log.d(TAG, "NPU/NNAPI available (legacy): $hasNNAPI")
        } catch (e: Exception) {
            Log.e(TAG, "Error reading NPU info (legacy)", e)
        }
        return npuInfo
    }

    fun getMemoryInfoLegacy(): JSONObject {
        val memInfo = JSONObject()
        try {
            val activityManager = context.getSystemService(Context.ACTIVITY_SERVICE) as ActivityManager
            val memoryInfo = ActivityManager.MemoryInfo()
            activityManager.getMemoryInfo(memoryInfo)

            val totalMB = memoryInfo.totalMem / (1024 * 1024)
            val availMB = memoryInfo.availMem / (1024 * 1024)
            val usedMB = totalMB - availMB

            memInfo.put("totalMB", totalMB)
            memInfo.put("availableMB", availMB)
            memInfo.put("usedMB", usedMB)
            memInfo.put("lowMemory", memoryInfo.lowMemory)
            memInfo.put("threshold", memoryInfo.threshold / (1024 * 1024))

            Log.d(TAG, "Memory (legacy): ${usedMB}/${totalMB} MB used")
        } catch (e: Exception) {
            Log.e(TAG, "Error reading memory info (legacy)", e)
        }
        return memInfo
    }

    fun getThermalInfoLegacy(): JSONObject {
        val thermalInfo = JSONObject()
        try {
            // Legacy: simple static response
            thermalInfo.put("status", "normal")
            thermalInfo.put("temperatureCelsius", 35.0)

            Log.d(TAG, "Thermal status (legacy): normal")
        } catch (e: Exception) {
            Log.e(TAG, "Error reading thermal info (legacy)", e)
        }
        return thermalInfo
    }

    fun getBatteryInfoLegacy(): JSONObject {
        val batteryInfo = JSONObject()
        try {
            batteryInfo.put("level", 80)
            batteryInfo.put("charging", false)
            batteryInfo.put("health", "good")

            Log.d(TAG, "Battery (legacy): 80%")
        } catch (e: Exception) {
            Log.e(TAG, "Error reading battery info (legacy)", e)
        }
        return batteryInfo
    }

    fun getAllSensorsLegacy(): JSONObject {
        val sensors = JSONObject()
        try {
            // Keep legacy hard-coded sensor presence for compatibility
            sensors.put("accelerometer", true)
            sensors.put("gyroscope", true)
            sensors.put("magnetometer", true)
            sensors.put("proximity", true)
            sensors.put("light", true)

            Log.d(TAG, "Sensors enumerated (legacy)")
        } catch (e: Exception) {
            Log.e(TAG, "Error reading sensors (legacy)", e)
        }
        return sensors
    }

    private fun hasGPULegacy(): Boolean {
        // Legacy always returned true
        return true
    }
    
    /**
     * Calculate Lambda (Λ) hardware score
     * 
     * Λ ∈ [10, 832] based on:
     * - CPU cores and frequency
     * - Memory capacity
     * - GPU availability
     * - NPU/NNAPI support
     * 
     * @return Lambda score [10-832]
     */
    fun calculateLambda(): Double {
        var lambda = 10.0 // Base score
        
        try {
            // CPU contribution (up to 300 points)
            val cpuInfo = getCPUInfo()
            val cores = cpuInfo.optInt("cores", 2)
            lambda += cores * 30.0 // 30 points per core
            
            // Memory contribution (up to 200 points)
            val memInfo = getMemoryInfo()
            val totalGB = memInfo.optLong("totalMB", 2048) / 1024.0
            lambda += totalGB * 40.0 // 40 points per GB
            
            // GPU contribution (up to 150 points)
            if (hasGPU()) {
                lambda += 150.0
            }
            
            // NPU/NNAPI contribution (up to 100 points)
            val npuInfo = getNPUInfo()
            if (npuInfo.optBoolean("nnapi_available", false)) {
                lambda += 100.0
            }
            
            // Device tier bonus (up to 82 points)
            val deviceTier = detectDeviceTier()
            lambda += deviceTier * 20.0
            
            // Clamp to [10, 832]
            lambda = lambda.coerceIn(10.0, 832.0)
            
            Log.i(TAG, "Calculated Lambda: $lambda")
        } catch (e: Exception) {
            Log.e(TAG, "Error calculating Lambda", e)
            lambda = 100.0 // Safe default
        }
        
        return lambda
    }
    
    /**
     * Check if device has GPU
     */
    private fun hasGPU(): Boolean {
        return try {
            val g = getGPUInfoTyped()
            !(g.renderer == "Unknown" && g.vendor == "Unknown")
        } catch (e: Exception) {
            true
        }
    }
    
    /**
     * Detect device tier (0-4)
     * 0 = Low-end, 4 = Flagship
     */
    private fun detectDeviceTier(): Int {
        val cores = Runtime.getRuntime().availableProcessors()
        val activityManager = context.getSystemService(Context.ACTIVITY_SERVICE) as ActivityManager
        val memInfo = ActivityManager.MemoryInfo()
        activityManager.getMemoryInfo(memInfo)
        val ramGB = memInfo.totalMem / (1024 * 1024 * 1024)
        
        return when {
            cores >= 8 && ramGB >= 8 -> 4 // Flagship
            cores >= 6 && ramGB >= 6 -> 3 // High-end
            cores >= 4 && ramGB >= 4 -> 2 // Mid-range
            cores >= 2 && ramGB >= 2 -> 1 // Low-mid
            else -> 0 // Entry-level
        }
    }
    
    /**
     * Read maximum CPU frequency
     */
    private fun readCPUMaxFrequency(): Long {
        return try {
            val file = File("/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq")
            if (file.exists()) {
                file.readText().trim().toLong() / 1000 // Convert to MHz
            } else {
                0L
            }
        } catch (e: Exception) {
            0L
        }
    }

    /* Non-destructive additions: typed getters + data classes
       These are added as extra APIs so existing JSON wrappers
       continue to work unchanged while new code can use typed
       structures. */

    fun getCPUInfoTyped(): CPUInfo {
        val cores = Runtime.getRuntime().availableProcessors()
        val architecture = System.getProperty("os.arch") ?: "unknown"
        val maxFreqKHz = try {
            val f = File("/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq")
            if (f.exists()) f.readText().trim().toLong() else 0L
        } catch (e: Exception) { 0L }
        return CPUInfo(cores = cores, maxFrequencyKHz = maxFreqKHz, architecture = architecture)
    }

    fun getGPUInfoTyped(): GPUInfo {
        // Use EGL/GLES only when supported; guard with API level and try/catch
        return try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.JELLY_BEAN_MR1) {
                val egl = EGL14.eglGetDisplay(EGL14.EGL_DEFAULT_DISPLAY)
                EGL14.eglInitialize(egl, null, 0, null, 0)
                val vendor = GLES20.glGetString(GLES20.GL_VENDOR) ?: "Unknown"
                val renderer = GLES20.glGetString(GLES20.GL_RENDERER) ?: "Unknown"
                val version = GLES20.glGetString(GLES20.GL_VERSION) ?: "Unknown"
                return GPUInfo(vendor = vendor, renderer = renderer, version = version)
            }
            GPUInfo()
        } catch (e: Exception) {
            GPUInfo()
        }
    }

    fun getNPUInfoTyped(): NPUInfo {
        val chipset = Build.HARDWARE.lowercase()
        val npuType = when {
            chipset.contains("qcom") || chipset.contains("qualcomm") -> "Hexagon DSP"
            chipset.contains("exynos") -> "NPU"
            chipset.contains("kirin") -> "NPU"
            chipset.contains("mt") || chipset.contains("mediatek") -> "APU"
            chipset.contains("unisoc") -> "NPU"
            else -> "Unknown"
        }
        val hasNNAPI = try { Class.forName("org.tensorflow.lite.nnapi.NnApiDelegate"); true } catch (_: Exception) { false }
        return NPUInfo(available = hasNNAPI && npuType != "Unknown", type = npuType, chipset = Build.HARDWARE)
    }

    fun getMemoryInfoTyped(): MemoryInfo {
        val activityManager = context.getSystemService<ActivityManager>() ?: return MemoryInfo()
        val memInfo = ActivityManager.MemoryInfo()
        activityManager.getMemoryInfo(memInfo)
        val total = memInfo.totalMem
        val avail = memInfo.availMem
        val used = total - avail
        return MemoryInfo(totalRAM = total, availableRAM = avail, usedRAM = used, lowMemory = memInfo.lowMemory, threshold = memInfo.threshold)
    }

    fun getThermalInfoTyped(): ThermalInfo {
        val batteryManager = context.getSystemService<BatteryManager>()
        val temperatureRaw = batteryManager?.getIntProperty(BatteryManager.BATTERY_PROPERTY_TEMPERATURE) ?: 250
        val celsius = temperatureRaw / 10.0
        val health = when {
            celsius < 40 -> 1.0
            celsius < 50 -> 1.0 - ((celsius - 40) / 20.0)
            celsius < 60 -> 0.5 - ((celsius - 50) / 20.0)
            else -> 0.0
        }
        val throttling = when {
            celsius > 55 -> Throttling.HIGH
            celsius > 45 -> Throttling.MODERATE
            else -> Throttling.NONE
        }
        return ThermalInfo(temperature = celsius, health = health.coerceIn(0.0,1.0), throttling = throttling)
    }

    fun getBatteryInfoTyped(): BatteryInfo {
        val batteryManager = context.getSystemService<BatteryManager>() ?: return BatteryInfo()
        val level = batteryManager.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY)
        val tempRaw = batteryManager.getIntProperty(BatteryManager.BATTERY_PROPERTY_TEMPERATURE)
        val temp = if (tempRaw != 0) tempRaw / 10.0 else 25.0
        val isCharging = try {
            val status = batteryManager.getIntProperty(BatteryManager.BATTERY_PROPERTY_STATUS)
            status == BatteryManager.BATTERY_STATUS_CHARGING || status == BatteryManager.BATTERY_STATUS_FULL
        } catch (e: Exception) { false }
        return BatteryInfo(level = level, isCharging = isCharging, temperature = temp)
    }

    /**
     * Typed sensor enumeration
     */
    fun getAllSensorsTyped(): List<Sensor> {
        val sensorManager = context.getSystemService<SensorManager>() ?: return emptyList()
        return sensorManager.getSensorList(Sensor.TYPE_ALL)
    }

    // Data classes (non-destructive additions)
    data class CPUInfo(
        val cores: Int = 0,
        val maxFrequencyKHz: Long = 0,
        val architecture: String = "unknown"
    )

    data class GPUInfo(
        val vendor: String = "Unknown",
        val renderer: String = "Unknown",
        val version: String = "Unknown"
    )

    data class NPUInfo(
        val available: Boolean = false,
        val type: String = "Unknown",
        val chipset: String = "Unknown"
    )

    data class MemoryInfo(
        val totalRAM: Long = 0,
        val availableRAM: Long = 0,
        val usedRAM: Long = 0,
        val lowMemory: Boolean = false,
        val threshold: Long = 0
    )

    data class ThermalInfo(
        val temperature: Double = 25.0,
        val health: Double = 1.0,
        val throttling: Throttling = Throttling.NONE
    )

    enum class Throttling {
        NONE,
        MODERATE,
        HIGH
    }

    data class BatteryInfo(
        val level: Int = 100,
        val isCharging: Boolean = false,
        val temperature: Double = 25.0
    )
}
