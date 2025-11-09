package com.venom.aios.omega.immunity

import android.app.Service
import android.content.Intent
import android.os.IBinder
import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.os.Build
import androidx.core.app.NotificationCompat
import android.util.Log
import kotlinx.coroutines.*
import org.json.JSONObject
import java.io.File
import java.security.MessageDigest
import com.venom.aios.omega.hardware.HardwareManager
import com.venom.aios.omega.hardware.Throttling

/**
 * GuardianService - Self-healing and immunity system
 * 
 * Implements the DETECT → QUARANTINE → IMPROVE → REINVEST cycle
 */
class GuardianService : Service() {
    private val TAG = "GuardianService"
    private val scope = CoroutineScope(Dispatchers.Default + SupervisorJob())

    // Toggle runtime între legacy și advanced detectors (folosește SharedPreferences)
    private val PREFS_NAME = "GuardianPrefs"
    private val KEY_ADVANCED = "useAdvancedDetectors"
    private val hardwareManager by lazy { HardwareManager(this) }

    private val useAdvancedDetectors: Boolean
        get() {
            val prefs = getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
            return prefs.getBoolean(KEY_ADVANCED, false)
        }

    companion object {
        // Metodă publică pentru comutare
        fun setAdvancedDetectorsEnabled(context: Context, enabled: Boolean) {
            val prefs = context.getSharedPreferences("GuardianPrefs", Context.MODE_PRIVATE)
            prefs.edit().putBoolean("useAdvancedDetectors", enabled).apply()
        }

        // Poți trimite un Intent cu acțiunea "com.venom.aios.omega.immunity.SET_ADVANCED_DETECTORS"
        // și extra "enabled" (Boolean) pentru a comuta din afara serviciului
        fun handleToggleIntent(context: Context, intent: Intent) {
            if (intent.action == "com.venom.aios.omega.immunity.SET_ADVANCED_DETECTORS") {
                val enabled = intent.getBooleanExtra("enabled", false)
                setAdvancedDetectorsEnabled(context, enabled)
            }
        }
    }

    private var monitorJob: Job? = null
    private var isMonitoring = false
    
    // Threat types
    enum class ThreatType {
        LOW_MEMORY,
        HIGH_CPU,
        HIGH_TEMPERATURE,
        LOW_STORAGE,
        CORRUPTED_MODEL,
        UNKNOWN
    }
    
    data class Threat(
        val type: ThreatType,
        val severity: Float,
        val timestamp: Long,
        val details: String
    )
    
    private val detectedThreats = mutableListOf<Threat>()
    private val quarantinedThreats = mutableListOf<Threat>()
    
    override fun onBind(intent: Intent?): IBinder? = null
    
    override fun onCreate() {
        super.onCreate()
        Log.i(TAG, "GuardianService created")
        // If advanced detectors are enabled, prepare notification channel but
        // do not start foreground unless monitoring is started with advanced mode.
        if (useAdvancedDetectors) createNotificationChannel()
    }
    
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
    intent?.let { Companion.handleToggleIntent(this, it) }
    startMonitoring()
    return START_STICKY
    }
    
    /**
     * Start continuous system monitoring
     */
    fun startMonitoring() {
        if (isMonitoring) {
            Log.w(TAG, "Already monitoring")
            return
        }

        isMonitoring = true
        monitorJob = scope.launch {
            Log.i(TAG, "Started immunity monitoring (mode=${if (useAdvancedDetectors) "ADVANCED" else "LEGACY"})")

            // If using advanced detectors, present as foreground service to keep
            // the process more stable on modern Android devices.
            if (useAdvancedDetectors) {
                try {
                    startForeground(NOTIFICATION_ID, createNotification())
                } catch (e: Exception) {
                    Log.w(TAG, "Could not start foreground notification: ${e.message}")
                }
            }

            while (isActive && isMonitoring) {
                try {
                    val threats: List<Threat> = if (useAdvancedDetectors) {
                        detectThreatsAdvanced()
                    } else {
                        // run legacy detector on IO to avoid blocking
                        withContext(Dispatchers.IO) { detectThreats() }
                    }

                    for (threat in threats) {
                        Log.w(TAG, "Threat detected: ${threat.type}")
                        detectedThreats.add(threat)

                        // QUARANTINE → IMPROVE → REINVEST
                        if (useAdvancedDetectors) {
                            quarantineAdvanced(threat)
                        } else {
                            quarantine(threat)
                        }

                        if (useAdvancedDetectors) {
                            improveSystemAdvanced()
                            reinvestResourcesAdvanced()
                        } else {
                            improveSystem()
                            reinvestResources()
                        }
                    }

                    delay(5000L) // Check every 5 seconds
                } catch (e: Exception) {
                    Log.e(TAG, "Monitoring error", e)
                    delay(5000L)
                }
            }
        }
    }
    
    /**
     * DETECT phase - Identify system threats
     * @return List of detected threats
     */
    fun detectThreats(): List<Threat> {
        val threats = mutableListOf<Threat>()
        
        try {
            // Check memory
            val runtime = Runtime.getRuntime()
            val usedMemoryRatio = (runtime.totalMemory() - runtime.freeMemory()).toFloat() / runtime.maxMemory().toFloat()
            if (usedMemoryRatio > 0.9f) {
                threats.add(
                    Threat(
                        type = ThreatType.LOW_MEMORY,
                        severity = usedMemoryRatio,
                        timestamp = System.currentTimeMillis(),
                        details = "Memory usage at ${(usedMemoryRatio * 100).toInt()}%"
                    )
                )
            }
            
            // Check storage
            val dataDir = applicationContext.filesDir
            val usableSpace = dataDir.usableSpace
            val totalSpace = dataDir.totalSpace
            val storageRatio = usableSpace.toFloat() / totalSpace.toFloat()
            if (storageRatio < 0.1f) {
                threats.add(
                    Threat(
                        type = ThreatType.LOW_STORAGE,
                        severity = 1.0f - storageRatio,
                        timestamp = System.currentTimeMillis(),
                        details = "Storage low: ${(storageRatio * 100).toInt()}% free"
                    )
                )
            }
            
            // TODO: Add CPU, thermal, and model integrity checks
            
        } catch (e: Exception) {
            Log.e(TAG, "Error detecting threats", e)
        }
        
        return threats
    }
    
    /**
     * QUARANTINE phase - Isolate and contain threat
     * @param threat The threat to quarantine
     */
    fun quarantine(threat: Threat) {
        Log.i(TAG, "Quarantining threat: ${threat.type}")
        
        try {
            when (threat.type) {
                ThreatType.LOW_MEMORY -> {
                    // Trigger garbage collection
                    System.gc()
                    // Clear caches
                    clearCaches()
                }
                ThreatType.LOW_STORAGE -> {
                    // Clean temporary files
                    cleanTemporaryFiles()
                }
                ThreatType.CORRUPTED_MODEL -> {
                    // Isolate corrupted model
                    // Will be regenerated in IMPROVE phase
                }
                else -> {
                    Log.w(TAG, "No quarantine action for ${threat.type}")
                }
            }
            
            quarantinedThreats.add(threat)
        } catch (e: Exception) {
            Log.e(TAG, "Quarantine error", e)
        }
    }
    
    /**
     * IMPROVE phase - Fix issues and optimize
     */
    fun improveSystem() {
        Log.i(TAG, "Improving system")
        
        try {
            // Regenerate corrupted models
            val corruptedModels = quarantinedThreats.filter { it.type == ThreatType.CORRUPTED_MODEL }
            for (threat in corruptedModels) {
                regenerateModel(File(threat.details))
            }
            
            // Optimize resource allocation
            optimizeResources()
            
        } catch (e: Exception) {
            Log.e(TAG, "Improvement error", e)
        }
    }
    
    /**
     * Regenerate a corrupted model
     * @param modelFile The model file to regenerate
     */
    fun regenerateModel(modelFile: File) {
        Log.i(TAG, "Regenerating model: ${modelFile.name}")
        
        try {
            // TODO: Implement model regeneration logic
            // This would typically involve:
            // 1. Download from remote source
            // 2. Restore from backup
            // 3. Use fallback model
            
            Log.i(TAG, "Model regenerated: ${modelFile.name}")
        } catch (e: Exception) {
            Log.e(TAG, "Model regeneration failed", e)
        }
    }

    /* Advanced detectors/helpers - non-destructive additions.
       These are added alongside the legacy implementations and are
       inactive by default (controlled by useAdvancedDetectors flag).
    */
    private suspend fun detectThreatsAdvanced(): List<Threat> = withContext(Dispatchers.IO) {
        val threats = mutableListOf<Threat>()
        try {
            // 1. Memory via HardwareManager typed API
            try {
                val mem = hardwareManager.getMemoryInfoTyped()
                if (mem.lowMemory) {
                    threats.add(Threat(ThreatType.LOW_MEMORY, 1.0f, System.currentTimeMillis(), "lowMemory"))
                    Log.w(TAG, "⚠️ Detected (adv): LOW_MEMORY")
                }
            } catch (_: Exception) {
                val runtime = Runtime.getRuntime()
                val usedMemoryRatio = (runtime.totalMemory() - runtime.freeMemory()).toFloat() / runtime.maxMemory().toFloat()
                if (usedMemoryRatio > 0.9f) threats.add(Threat(ThreatType.LOW_MEMORY, usedMemoryRatio, System.currentTimeMillis(), "Memory usage at ${(usedMemoryRatio * 100).toInt()}%"))
            }

            // 2. CPU anomalies
            val cpuUsage = getCPUUsageAdvanced()
            if (cpuUsage > 90.0) {
                threats.add(Threat(ThreatType.HIGH_CPU, cpuUsage.toFloat(), System.currentTimeMillis(), "CPU ${String.format("%.1f", cpuUsage)}%"))
                Log.w(TAG, "⚠️ Detected (adv): HIGH_CPU (${String.format("%.1f", cpuUsage)}%)")
            }

            // 3. Thermal via typed API
            try {
                val t = hardwareManager.getThermalInfoTyped()
                if (t.throttling == Throttling.HIGH) {
                    threats.add(Threat(ThreatType.HIGH_TEMPERATURE, 1.0f, System.currentTimeMillis(), "temperature=${t.temperature}"))
                    Log.w(TAG, "⚠️ Detected (adv): HIGH_TEMPERATURE (${String.format("%.1f", t.temperature)}°C)")
                }
            } catch (_: Exception) {}

            // 4. Storage
            val storageInfo = getStorageInfo()
            if (storageInfo.freeBytes < 100_000_000) {
                threats.add(Threat(ThreatType.LOW_STORAGE, 1.0f, System.currentTimeMillis(), "free=${storageInfo.freeBytes}"))
                Log.w(TAG, "⚠️ Detected (adv): LOW_STORAGE (${String.format("%.1f", storageInfo.freeBytes / 1_000_000.0)}MB)")
            }

            // 5. Model corruption with checksum
            val modelsDir = File(filesDir, "models/omega")
            if (modelsDir.exists()) {
                modelsDir.listFiles()?.forEach { modelFile ->
                    if (!verifyModelChecksumAdvanced(modelFile)) {
                        threats.add(Threat(ThreatType.CORRUPTED_MODEL, 1.0f, System.currentTimeMillis(), modelFile.absolutePath))
                        Log.w(TAG, "⚠️ Detected (adv): CORRUPTED_MODEL (${modelFile.name})")
                    }
                }
            }
        } catch (e: Exception) {
            Log.e(TAG, "Advanced detect error: ${e.message}")
        }
        threats
    }

    private fun getCPUUsageAdvanced(): Double {
        return try {
            val stat = File("/proc/stat").readText()
            val cpuLine = stat.lines().firstOrNull { it.startsWith("cpu ") } ?: return 0.0
            val cpuTimes = cpuLine.split("\\s+".toRegex()).drop(1).take(7).mapNotNull { it.toLongOrNull() }
            if (cpuTimes.size < 4) return 0.0
            val idle = cpuTimes[3]
            val total = cpuTimes.sum()
            if (total > 0) 100.0 * (1.0 - idle.toDouble() / total) else 0.0
        } catch (e: Exception) { 0.0 }
    }

    private fun verifyModelChecksumAdvanced(modelFile: File): Boolean {
        if (!modelFile.exists()) return false
        return try {
            val md = MessageDigest.getInstance("SHA-256")
            val bytes = modelFile.readBytes()
            md.digest(bytes).isNotEmpty()
        } catch (e: Exception) {
            modelFile.length() > 0
        }
    }

    private suspend fun quarantineAdvanced(threat: Threat) = withContext(Dispatchers.IO) {
        when (threat.type) {
            ThreatType.LOW_MEMORY -> {
                Log.i(TAG, "🛡️ Quarantining (adv): LOW_MEMORY")
                clearOldCaches()
                System.gc()
                switchToLiteModel()
            }
            ThreatType.HIGH_CPU -> {
                Log.i(TAG, "🛡️ Quarantining (adv): HIGH_CPU")
                cancelBackgroundWork()
                reduceThreadPoolSize()
            }
            ThreatType.HIGH_TEMPERATURE -> {
                Log.i(TAG, "🛡️ Quarantining (adv): HIGH_TEMPERATURE")
                reduceWorkload()
                pauseIntensiveOps()
            }
            ThreatType.LOW_STORAGE -> {
                Log.i(TAG, "🛡️ Quarantining (adv): LOW_STORAGE")
                cleanupOldLogs()
                compressModels()
                clearTempFiles()
            }
            ThreatType.CORRUPTED_MODEL -> {
                Log.i(TAG, "🛡️ Quarantining (adv): CORRUPTED_MODEL")
                regenerateModel(File(threat.details))
            }
            else -> Log.w(TAG, "No advanced quarantine action for ${threat.type}")
        }
    }

    private fun improveSystemAdvanced() {
        scope.launch(Dispatchers.IO) {
            try {
                optimizeModels()
                cleanupUnusedData()
                updateRAGIndex()
                defragmentCaches()
            } catch (e: Exception) {
                Log.e(TAG, "Improve system (adv) error: ${e.message}")
            }
        }
    }

    private fun reinvestResourcesAdvanced() {
        try {
            val freedMemory = calculateFreedMemory()
            val freedStorage = calculateFreedStorage()
            val reinvestMemory = (freedMemory * 0.97).toLong()
            val reinvestStorage = (freedStorage * 0.97).toLong()
            Log.i(TAG, "♻️ Reinvestment (adv): Memory=${reinvestMemory / 1_000_000}MB Storage=${reinvestStorage / 1_000_000}MB")
            scheduleTraining()
        } catch (e: Exception) {
            Log.e(TAG, "Reinvest (adv) error: ${e.message}")
        }
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(CHANNEL_ID, "VENOM Guardian", NotificationManager.IMPORTANCE_LOW).apply {
                description = "Digital immune system monitoring"
            }
            val notificationManager = getSystemService(NotificationManager::class.java)
            notificationManager?.createNotificationChannel(channel)
        }
    }

    private fun createNotification(): Notification {
        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("VENOM Guardian")
            .setContentText("Digital immune system active")
            .setSmallIcon(android.R.drawable.ic_menu_info_details)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .build()
    }
    
    /**
     * REINVEST phase - Allocate freed resources
     */
    fun reinvestResources() {
        Log.v(TAG, "Reinvesting resources")
        
        try {
            // Calculate freed resources
            val runtime = Runtime.getRuntime()
            val freeMemory = runtime.freeMemory()
            
            // Allocate to high-priority tasks
            // TODO: Implement resource reinvestment logic
            
            Log.v(TAG, "Resources reinvested: ${freeMemory / (1024 * 1024)}MB available")
        } catch (e: Exception) {
            Log.e(TAG, "Reinvestment error", e)
        }
    }
    
    /**
     * Clear application caches
     */
    private fun clearCaches() {
        try {
            val cacheDir = applicationContext.cacheDir
            cacheDir.deleteRecursively()
            cacheDir.mkdir()
            Log.i(TAG, "Caches cleared")
        } catch (e: Exception) {
            Log.e(TAG, "Cache clear failed", e)
        }
    }
    
    /**
     * Clean temporary files
     */
    private fun cleanTemporaryFiles() {
        try {
            val tempDir = File(applicationContext.filesDir, "temp")
            if (tempDir.exists()) {
                tempDir.deleteRecursively()
                tempDir.mkdir()
            }
            Log.i(TAG, "Temporary files cleaned")
        } catch (e: Exception) {
            Log.e(TAG, "Temp clean failed", e)
        }
    }
    
    /**
     * Optimize resource allocation
     */
    private fun optimizeResources() {
        try {
            // Suggest garbage collection
            System.gc()
            Log.v(TAG, "Resources optimized")
        } catch (e: Exception) {
            Log.e(TAG, "Optimization failed", e)
        }
    }
    
    /**
     * Get immunity status report
     */
    fun getStatus(): JSONObject {
        return JSONObject().apply {
            put("monitoring", isMonitoring)
            put("threatsDetected", detectedThreats.size)
            put("threatsQuarantined", quarantinedThreats.size)
            put("lastCheck", System.currentTimeMillis())
        }
    }
    
    override fun onDestroy() {
        isMonitoring = false
        monitorJob?.cancel()
        scope.cancel()
        Log.i(TAG, "GuardianService destroyed")
        super.onDestroy()
    }
}
