package com.venom.aios.omega.hardware

import android.app.ActivityManager
import android.content.Context
import android.os.Build
import android.util.Log
import org.json.JSONObject
import java.io.File

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
            val nCores = Runtime.getRuntime().availableProcessors()
            val cpuAbi = Build.SUPPORTED_ABIS.joinToString(", ")
            
            cpuInfo.put("cores", nCores)
            cpuInfo.put("abi", cpuAbi)
            cpuInfo.put("architecture", System.getProperty("os.arch") ?: "unknown")
            
            // Read CPU frequency if available
            val maxFreq = readCPUMaxFrequency()
            if (maxFreq > 0) {
                cpuInfo.put("maxFrequencyMHz", maxFreq)
            }
            
            Log.d(TAG, "CPU Info: $nCores cores, $cpuAbi")
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
            // Android doesn't provide direct GPU info easily
            // We can infer from device model and OpenGL ES version
            gpuInfo.put("renderer", "unknown")
            gpuInfo.put("vendor", "unknown")
            gpuInfo.put("available", hasGPU())
            
            Log.d(TAG, "GPU available: ${hasGPU()}")
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
            // Check for NNAPI support (Neural Networks API)
            val hasNNAPI = Build.VERSION.SDK_INT >= Build.VERSION_CODES.O_MR1
            npuInfo.put("nnapi_available", hasNNAPI)
            npuInfo.put("nnapi_version", if (hasNNAPI) Build.VERSION.SDK_INT else 0)
            
            Log.d(TAG, "NPU/NNAPI available: $hasNNAPI")
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
            
            Log.d(TAG, "Memory: ${usedMB}/${totalMB} MB used")
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
            // Basic thermal info - can be expanded with actual thermal API
            thermalInfo.put("status", "normal")
            thermalInfo.put("temperatureCelsius", 35.0)
            
            Log.d(TAG, "Thermal status: normal")
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
            // TODO: Implement battery level reading via BatteryManager
            batteryInfo.put("level", 80)
            batteryInfo.put("charging", false)
            batteryInfo.put("health", "good")
            
            Log.d(TAG, "Battery: 80%")
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
            // TODO: Enumerate actual sensors using SensorManager
            sensors.put("accelerometer", true)
            sensors.put("gyroscope", true)
            sensors.put("magnetometer", true)
            sensors.put("proximity", true)
            sensors.put("light", true)
            
            Log.d(TAG, "Sensors enumerated")
        } catch (e: Exception) {
            Log.e(TAG, "Error reading sensors", e)
        }
        
        return sensors
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
        // Most Android devices have GPU, but we can check more specifically
        return true // TODO: Implement more specific GPU detection
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
}
