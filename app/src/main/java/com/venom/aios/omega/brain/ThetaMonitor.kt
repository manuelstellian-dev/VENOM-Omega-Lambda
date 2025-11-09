package com.venom.aios.omega.brain

import android.app.ActivityManager
import android.content.Context
import android.os.Build
import android.util.Log
import com.venom.aios.omega.hardware.HardwareManager
import kotlinx.coroutines.*
import java.io.RandomAccessFile

/**
 * ThetaMonitor - Continuous monitoring and calculation of theta (θ)
 * 
 * Formula: θ = 0.3 × H_CPU + 0.3 × H_MEM + 0.4 × H_TERM
 * Where H_* are normalized health metrics [0.0-1.0]
 */
class ThetaMonitor(private val context: Context) {
    private val TAG = "ThetaMonitor"
    private val scope = CoroutineScope(Dispatchers.Default + SupervisorJob())
    
    private var isMonitoring = false
    private var monitorJob: Job? = null
    private val hardwareManager = HardwareManager(context)
    
    // Current health metrics
    private var cpuHealth: Double = 0.8
    private var memHealth: Double = 0.8
    private var thermalHealth: Double = 0.8
    private var currentTheta: Double = 0.8
    
    // Callbacks
    private val thetaCallbacks = mutableListOf<(Double) -> Unit>()
    
    /**
     * Start continuous theta monitoring
     * @param intervalMs Monitoring interval in milliseconds
     */
    fun start(intervalMs: Long = 1000L) {
        if (isMonitoring) {
            Log.w(TAG, "Monitor already running")
            return
        }
        
        isMonitoring = true
        monitorJob = scope.launch {
            Log.i(TAG, "Started theta monitoring (interval=${intervalMs}ms)")
            while (isActive && isMonitoring) {
                try {
                    cpuHealth = getCPUHealth()
                    memHealth = getMemoryHealth()
                    thermalHealth = getThermalHealth()
                    
                    currentTheta = calculateTheta()
                    
                    // Notify callbacks
                    thetaCallbacks.forEach { callback ->
                        try {
                            callback(currentTheta)
                        } catch (e: Exception) {
                            Log.e(TAG, "Callback error", e)
                        }
                    }
                    
                    delay(intervalMs)
                } catch (e: Exception) {
                    Log.e(TAG, "Monitoring error", e)
                }
            }
        }
    }
    
    /**
     * Stop theta monitoring
     */
    fun stop() {
        isMonitoring = false
        monitorJob?.cancel()
        Log.i(TAG, "Stopped theta monitoring")
    }
    
    /**
     * Subscribe to theta updates
     * @param callback Function to call with new theta values
     */
    fun subscribeToTheta(callback: (Double) -> Unit) {
        thetaCallbacks.add(callback)
    }
    
    /**
     * Calculate theta from current health metrics
     * θ = 0.3 × H_CPU + 0.3 × H_MEM + 0.4 × H_TERM
     * 
     * @return Current theta value [0.0-1.0]
     */
    fun calculateTheta(): Double {
        val theta = 0.3 * cpuHealth + 0.3 * memHealth + 0.4 * thermalHealth
        Log.v(TAG, "Theta calculated: $theta (CPU=$cpuHealth, MEM=$memHealth, TERM=$thermalHealth)")
        return theta.coerceIn(0.0, 1.0)
    }
    
    /**
     * Get CPU health metric
     * @return CPU health [0.0-1.0], where 1.0 is optimal
     */
    fun getCPUHealth(): Double {
        return try {
            val cpuUsage = readCPUUsage()
            // Convert usage to health (inverse relationship)
            (1.0 - cpuUsage).coerceIn(0.0, 1.0)
        } catch (e: Exception) {
            Log.e(TAG, "Error reading CPU health", e)
            0.7 // Default fallback
        }
    }
    
    /**
     * Get memory health metric
     * @return Memory health [0.0-1.0], where 1.0 is optimal
     */
    fun getMemoryHealth(): Double {
        return try {
            val mem = hardwareManager.getMemoryInfoTyped()
            if (mem.totalRAM > 0L) {
                val availableRatio = mem.availableRAM.toDouble() / mem.totalRAM.toDouble()
                return availableRatio.coerceIn(0.0, 1.0)
            }

            // Fallback: try direct ActivityManager read if typed getter returned no data
            try {
                val activityManager = context.getSystemService(Context.ACTIVITY_SERVICE) as ActivityManager
                val memInfo = ActivityManager.MemoryInfo()
                activityManager.getMemoryInfo(memInfo)
                val availableRatio = memInfo.availMem.toDouble() / memInfo.totalMem.toDouble()
                return availableRatio.coerceIn(0.0, 1.0)
            } catch (_: Exception) {
                // ignore and fall through to default
            }

            0.7
        } catch (e: Exception) {
            Log.e(TAG, "Error reading memory health", e)
            0.7 // Default fallback
        }
    }
    
    /**
     * Get thermal health metric
     * @return Thermal health [0.0-1.0], where 1.0 is cool
     */
    fun getThermalHealth(): Double {
        return try {
            val t = hardwareManager.getThermalInfoTyped()
            // If typed getter gives a sensible value, use it
            if (t.health in 0.0..1.0) return t.health.coerceIn(0.0, 1.0)

            // Fallback to older logic: use platform thermal service or battery temp
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                try {
                    val thermalStatus = context.getSystemService(Context.THERMAL_SERVICE)
                    // best-effort: if platform service exists, we prefer it — but legacy default below
                    return 0.8
                } catch (_: Exception) {
                    // continue to battery temp fallback
                }
            }

            // Battery temp fallback
            val temp = readBatteryTemperature()
            calculateThermalHealthFromTemp(temp)
        } catch (e: Exception) {
            Log.e(TAG, "Error reading thermal health", e)
            0.7 // Default fallback
        }
    }

    /** Legacy (non-destructive) methods kept for compatibility. */
    fun getMemoryHealthLegacy(): Double {
        return try {
            val activityManager = context.getSystemService(Context.ACTIVITY_SERVICE) as ActivityManager
            val memInfo = ActivityManager.MemoryInfo()
            activityManager.getMemoryInfo(memInfo)

            val availableRatio = memInfo.availMem.toDouble() / memInfo.totalMem.toDouble()
            availableRatio.coerceIn(0.0, 1.0)
        } catch (e: Exception) {
            Log.e(TAG, "Error reading memory health (legacy)", e)
            0.7
        }
    }

    fun getThermalHealthLegacy(): Double {
        return try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                val thermalStatus = context.getSystemService(Context.THERMAL_SERVICE)
                // TODO: Implement proper thermal API usage (legacy returned a safe default)
                0.8
            } else {
                val temp = readBatteryTemperature()
                calculateThermalHealthFromTemp(temp)
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error reading thermal health (legacy)", e)
            0.7
        }
    }
    
    /**
     * Read CPU usage from /proc/stat
     * @return CPU usage [0.0-1.0]
     */
    private fun readCPUUsage(): Double {
        return try {
            val reader = RandomAccessFile("/proc/stat", "r")
            val load = reader.readLine()
            reader.close()
            
            val tokens = load.split("\\s+".toRegex())
            val idle = tokens[4].toLong()
            val total = tokens.slice(1..7).sumOf { it.toLong() }
            
            val usage = 1.0 - (idle.toDouble() / total.toDouble())
            usage.coerceIn(0.0, 1.0)
        } catch (e: Exception) {
            0.5 // Default to 50% usage if unable to read
        }
    }
    
    /**
     * Read battery temperature
     * @return Temperature in Celsius
     */
    private fun readBatteryTemperature(): Float {
        // TODO: Implement battery temperature reading
        // For now, return a safe default
        return 35.0f
    }
    
    /**
     * Calculate thermal health from temperature
     * @param tempCelsius Temperature in Celsius
     * @return Thermal health [0.0-1.0]
     */
    private fun calculateThermalHealthFromTemp(tempCelsius: Float): Double {
        return when {
            tempCelsius < 30 -> 1.0
            tempCelsius < 40 -> 0.8
            tempCelsius < 50 -> 0.5
            else -> 0.3
        }.coerceIn(0.0, 1.0)
    }
    
    /**
     * Get current theta value
     */
    fun getCurrentTheta(): Double = currentTheta
    
    /**
     * Cleanup resources
     */
    fun cleanup() {
        stop()
        scope.cancel()
        thetaCallbacks.clear()
    }
}
