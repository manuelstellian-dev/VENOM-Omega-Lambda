package com.venom.aios

import android.app.Application
import android.util.Log
import java.io.File

/**
 * VenomApplication - Main Application class for VENOM Ω-AIOS
 * 
 * Initializes the organism's directory structure and core components.
 * This is the entry point for the Android application lifecycle.
 */
class VenomApplication : Application() {
    
    private val TAG = "VenomApplication"
    
    override fun onCreate() {
        super.onCreate()
        Log.i(TAG, "🧬 VENOM Organism Birth Initiated...")
        
        // Initialize directory structure
        initializeDirectories()
        
        // Initialize core components
        initializeCoreComponents()
        
        Log.i(TAG, "✅ VENOM Organism Birth Complete")
    }
    
    /**
     * Initialize the directory structure for VENOM
     */
    private fun initializeDirectories() {
        try {
            val baseDir = filesDir
            
            // Create essential directories
            val directories = listOf(
                File(baseDir, "models"),        // For LLM models
                File(baseDir, "knowledge"),     // For RAG vector database
                File(baseDir, "cache"),         // For temporary data
                File(baseDir, "logs"),          // For application logs
                File(baseDir, "quarantine"),    // For Guardian Service
                File(baseDir, "checkpoints")    // For state snapshots
            )
            
            directories.forEach { dir ->
                if (!dir.exists()) {
                    val created = dir.mkdirs()
                    if (created) {
                        Log.d(TAG, "📁 Created directory: ${dir.name}")
                    } else {
                        Log.w(TAG, "⚠️ Failed to create directory: ${dir.name}")
                    }
                } else {
                    Log.d(TAG, "📁 Directory exists: ${dir.name}")
                }
            }
            
            // Create .nomedia files to prevent media scanning
            val noMediaDirs = listOf("models", "knowledge", "cache", "quarantine")
            noMediaDirs.forEach { dirName ->
                val noMediaFile = File(File(baseDir, dirName), ".nomedia")
                if (!noMediaFile.exists()) {
                    noMediaFile.createNewFile()
                }
            }
            
            Log.i(TAG, "✅ Directory structure initialized")
            
        } catch (e: Exception) {
            Log.e(TAG, "❌ Failed to initialize directories", e)
        }
    }
    
    /**
     * Initialize core components
     */
    private fun initializeCoreComponents() {
        try {
            // Set global exception handler
            Thread.setDefaultUncaughtExceptionHandler { thread, throwable ->
                Log.e(TAG, "💥 Uncaught exception in thread ${thread.name}", throwable)
                // In production, this would trigger self-healing mechanisms
            }
            
            Log.i(TAG, "✅ Core components initialized")
            
        } catch (e: Exception) {
            Log.e(TAG, "❌ Failed to initialize core components", e)
        }
    }
    
    override fun onTerminate() {
        super.onTerminate()
        Log.i(TAG, "☠️ VENOM Organism Terminating...")
    }
    
    override fun onLowMemory() {
        super.onLowMemory()
        Log.w(TAG, "⚠️ Low memory condition detected - triggering conservation protocols")
        // Trigger entropy engine's resource conservation
    }
    
    override fun onTrimMemory(level: Int) {
        super.onTrimMemory(level)
        Log.w(TAG, "⚠️ Memory trim requested - level: $level")
        
        when (level) {
            TRIM_MEMORY_RUNNING_CRITICAL,
            TRIM_MEMORY_COMPLETE -> {
                // Aggressive cleanup
                Log.w(TAG, "🔥 Critical memory pressure - aggressive cleanup")
            }
            TRIM_MEMORY_RUNNING_LOW,
            TRIM_MEMORY_MODERATE -> {
                // Moderate cleanup
                Log.w(TAG, "⚠️ Moderate memory pressure - conservative cleanup")
            }
        }
    }
}
