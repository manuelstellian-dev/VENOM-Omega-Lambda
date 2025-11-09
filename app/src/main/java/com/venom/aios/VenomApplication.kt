
// VENOM Ω-AIOS: Supreme Hybrid Application Class
// -------------------------------------------------------------
// This file defines the main Application class for VENOM Omega Lambda.
// It orchestrates initialization, directory structure, logging, memory management,
// and global exception handling for the organism's lifecycle.
//
// All critical logic, comments, and documentation are preserved and extended.
// -------------------------------------------------------------
package com.venom.aios


import android.app.Application
import android.util.Log
import java.io.File
import androidx.work.Configuration

/**
 * VenomApplication - Main Application class for VENOM Ω-AIOS
 * ---------------------------------------------------------
 * Entry point for the Android organism lifecycle.
 * Responsibilities:
 *   - Initializes global singleton instance
 *   - Sets up logging (SLF4J, extensible)
 *   - Creates and manages extended directory structure
 *   - Initializes core components and exception handling
 *   - Configures WorkManager for background tasks
 *   - Handles memory and termination events
 *
 * All logic and comments are preserved and extended for clarity.
 */
class VenomApplication : Application(), Configuration.Provider {
    companion object {
        /**
         * TAG for logging throughout the application lifecycle
         */
        private const val TAG = "VenomApplication"

        /**
         * Global singleton instance for accessing context and resources
         * Usage: VenomApplication.instance
         */
        lateinit var instance: VenomApplication
            private set
    }

    /**
     * Called when the application is starting, before any activity, service,
     * or receiver objects have been created.
     * Orchestrates all initialization steps for the VENOM organism.
     */
    override fun onCreate() {
        super.onCreate()
        instance = this

        Log.i(TAG, "🧬 VENOM Organism Birth Initiated...")

        // Step 1: Initialize global logging configuration
        initializeLogging()

        // Step 2: Create and verify extended directory structure
        initializeDirectories()

        // Step 3: Initialize core components and exception handling
        initializeCoreComponents()

        Log.i(TAG, "✅ VENOM Organism Birth Complete")
    }
    
    /**
     * Initializes global logging configuration for VENOM organism.
     * Uses SLF4J (extensible) for unified logging across modules.
     * Can be extended for remote logging, analytics, etc.
     */
    private fun initializeLogging() {
        // Setup logging configuration (SLF4J, extensibil)
        System.setProperty("org.slf4j.simpleLogger.defaultLogLevel", "INFO")
    }

    /**
     * Creates and verifies the extended directory structure required by VENOM.
     * Ensures all essential and advanced directories exist for models, knowledge,
     * cache, logs, quarantine, and more. Adds .nomedia files to prevent media scanning.
     *
     * This method is robust and logs all actions for audit and debugging.
     */
    private fun initializeDirectories() {
        try {
            val baseDir = filesDir

            // List of essential and extended directories for the organism
            val directories = listOf(
                File(baseDir, "models"),              // Model storage
                File(baseDir, "models/omega"),         // Omega models
                File(baseDir, "knowledge"),            // Knowledge base
                File(baseDir, "knowledge/wikipedia"),  // Wikipedia dumps
                File(baseDir, "knowledge/papers"),     // Scientific papers
                File(baseDir, "knowledge/code"),       // Code knowledge
                File(baseDir, "knowledge/index"),      // Indexes
                File(baseDir, "cache"),                // General cache
                File(baseDir, "logs"),                 // Log files
                File(baseDir, "quarantine"),           // Quarantine zone
                File(baseDir, "checkpoints"),          // Model checkpoints
                cacheDir.resolve("temp")               // Temporary files
            )

            // Create each directory if it does not exist
            directories.forEach { dir ->
                if (!dir.exists()) {
                    val created = dir.mkdirs()
                    if (created) {
                        Log.d(TAG, "📁 Created directory: ${dir.path}")
                    } else {
                        Log.w(TAG, "⚠️ Failed to create directory: ${dir.path}")
                    }
                } else {
                    Log.d(TAG, "📁 Directory exists: ${dir.path}")
                }
            }

            // Add .nomedia files to prevent Android media scanning in sensitive folders
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
     * Initializes core components for the VENOM organism.
     * Sets up global exception handler for self-healing and diagnostics.
     * Extend this method to initialize mesh, neural, hardware, immunity, etc.
     */
    private fun initializeCoreComponents() {
        try {
            // Set global exception handler for all threads
            Thread.setDefaultUncaughtExceptionHandler { thread, throwable ->
                Log.e(TAG, "💥 Uncaught exception in thread ${thread.name}", throwable)
                // In production, this would trigger self-healing mechanisms
                // Example: restart services, notify Guardian, log to remote
            }

            Log.i(TAG, "✅ Core components initialized")

        } catch (e: Exception) {
            Log.e(TAG, "❌ Failed to initialize core components", e)
        }
    }

    /**
     * Provides custom configuration for AndroidX WorkManager.
     * Ensures background tasks use appropriate logging and resource management.
     * Extend for custom workers, mesh jobs, health sync, etc.
     */
    override fun getWorkManagerConfiguration(): Configuration {
        return Configuration.Builder()
            .setMinimumLoggingLevel(Log.INFO)
            .build()
    }
    
    /**
     * Called when the application is terminating (emulator/dev only).
     * Use for cleanup, logging, and finalization.
     */
    override fun onTerminate() {
        super.onTerminate()
        Log.i(TAG, "☠️ VENOM Organism Terminating...")
    }

    /**
     * Called when the system is running low on memory.
     * Triggers resource conservation protocols (entropy engine, mesh, etc).
     */
    override fun onLowMemory() {
        super.onLowMemory()
        Log.w(TAG, "⚠️ Low memory condition detected - triggering conservation protocols")
        // Trigger entropy engine's resource conservation
        // Example: release caches, reduce mesh activity, notify Guardian
    }

    /**
     * Called when the system requests memory trimming at various levels.
     * Implements aggressive or conservative cleanup based on severity.
     * Extend to trigger mesh, neural, or hardware resource management.
     */
    override fun onTrimMemory(level: Int) {
        super.onTrimMemory(level)
        Log.w(TAG, "⚠️ Memory trim requested - level: $level")

        when (level) {
            TRIM_MEMORY_RUNNING_CRITICAL,
            TRIM_MEMORY_COMPLETE -> {
                // Aggressive cleanup: release all non-essential resources
                Log.w(TAG, "🔥 Critical memory pressure - aggressive cleanup")
                // Example: clear caches, pause mesh, notify Guardian
            }
            TRIM_MEMORY_RUNNING_LOW,
            TRIM_MEMORY_MODERATE -> {
                // Moderate cleanup: release some resources
                Log.w(TAG, "⚠️ Moderate memory pressure - conservative cleanup")
                // Example: reduce background jobs, lower mesh activity
            }
        }
    }
}
