package com.venom.aios.main

import android.content.Context
import android.util.Log
import com.venom.aios.integration.OmegaLambdaBridge
import com.venom.aios.omega.brain.*
import com.venom.aios.omega.hardware.HardwareManager
import com.venom.aios.omega.immunity.GuardianService
import com.venom.aios.omega.neural.LLMEngine
import com.venom.aios.omega.knowledge.RAGEngine
import com.venom.aios.omega.tetrastrat.*
import kotlinx.coroutines.*
import org.json.JSONObject

/**
 * OrganismVitals - System vitals data class
 */
data class OrganismVitals(
    val theta: Double,
    val lambdaScore: Double,
    val meshNodes: Int,
    val meshMessagesPending: Int,
    val cpuHealth: Double,
    val memoryUsage: Double,
    val thermalHealth: Double,
    val batteryLevel: Int,
    val isAlive: Boolean
)

/**
 * VenomOrganism - The complete VENOM system orchestrator
 * 
 * Singleton that manages the lifecycle of both Ω-AIOS and Λ-Genesis layers
 */
class VenomOrganism private constructor(private val context: Context) {
    private val TAG = "VenomOrganism"
    private val scope = CoroutineScope(Dispatchers.Default + SupervisorJob())
    
    // Omega components
    private val omegaArbiter = OmegaArbiter()
    private val mobiusEngine = AdaptiveMobiusEngine()
    private val thetaMonitor = ThetaMonitor(context)
    private val hardwareManager = HardwareManager(context)
    private val llmEngine = LLMEngine(context)
    private val ragEngine = RAGEngine(context)
    
    // Tetrastrat engines
    private val optimizeEngine = OptimizeEngine()
    private val balanceEngine = BalanceEngine()
    private val regenerateEngine = RegenerateEngine()
    private val entropyEngine = EntropyEngine()
    
    // Integration bridge
    private lateinit var bridge: OmegaLambdaBridge
    
    // State
    private var isAlive = false
    private var vitalsJob: Job? = null
    private var currentVitals: OrganismVitals? = null
    
    companion object {
        @Volatile
        private var instance: VenomOrganism? = null
        
        fun getInstance(context: Context): VenomOrganism {
            return instance ?: synchronized(this) {
                instance ?: VenomOrganism(context.applicationContext).also {
                    instance = it
                }
            }
        }
    }
    
    /**
     * Birth - Initialize and start the organism
     */
    suspend fun birth(): Boolean = withContext(Dispatchers.Default) {
        if (isAlive) {
            Log.w(TAG, "Organism already alive")
            return@withContext true
        }
        
        try {
            Log.i(TAG, "🌱 VENOM Organism birth sequence initiated...")
            
            // Initialize hardware and auto-configure
            Log.d(TAG, "Configuring Möbius engine...")
            mobiusEngine.autoConfigureFromHardware()
            mobiusEngine.demo()
            
            // Start theta monitoring
            Log.d(TAG, "Starting theta monitor...")
            thetaMonitor.start()
            
            // Initialize LLM and RAG engines
            Log.d(TAG, "Loading AI engines...")
            llmEngine.loadModel()
            ragEngine.loadKnowledgeBase()
            
            // Initialize Omega-Lambda bridge
            Log.d(TAG, "Building Ω ↔ Λ bridge...")
            bridge = OmegaLambdaBridge(context, omegaArbiter, thetaMonitor, hardwareManager)
            
            if (bridge.initializePython()) {
                Log.d(TAG, "Python environment ready")
                bridge.importLambdaModules()
                bridge.startLambdaOrganism()
                bridge.populateNanobots(10)
                bridge.startHealthSync()
            } else {
                Log.w(TAG, "Python initialization failed, continuing in Omega-only mode")
            }
            
            isAlive = true
            Log.i(TAG, "✨ VENOM Organism is ALIVE")
            
            true
        } catch (e: Exception) {
            Log.e(TAG, "Birth sequence failed", e)
            false
        }
    }
    
    /**
     * Start vitals monitoring
     */
    fun startVitalsMonitoring(callback: (OrganismVitals) -> Unit) {
        if (vitalsJob != null) {
            Log.w(TAG, "Vitals monitoring already running")
            return
        }
        
        vitalsJob = scope.launch {
            while (isActive && isAlive) {
                try {
                    val vitals = collectVitals()
                    currentVitals = vitals
                    callback(vitals)
                    delay(1000L)
                } catch (e: Exception) {
                    Log.e(TAG, "Vitals collection error", e)
                    delay(1000L)
                }
            }
        }
    }
    
    /**
     * Collect current vitals
     */
    private suspend fun collectVitals(): OrganismVitals = withContext(Dispatchers.IO) {
        val theta = thetaMonitor.getCurrentTheta()
        val lambda = hardwareManager.calculateLambda()
        
        val meshVitals = try {
            bridge.getMeshVitals()
        } catch (e: Exception) {
            JSONObject()
        }
        
        OrganismVitals(
            theta = theta,
            lambdaScore = lambda,
            meshNodes = meshVitals.optInt("nodes", 0),
            meshMessagesPending = meshVitals.optInt("messages", 0),
            cpuHealth = thetaMonitor.getCPUHealth(),
            memoryUsage = 1.0 - thetaMonitor.getMemoryHealth(),
            thermalHealth = thetaMonitor.getThermalHealth(),
            batteryLevel = 80, // TODO: Get actual battery level
            isAlive = isAlive
        )
    }
    
    /**
     * Get current vitals synchronously
     */
    fun getVitals(): OrganismVitals {
        return currentVitals ?: OrganismVitals(
            theta = 0.7,
            lambdaScore = 100.0,
            meshNodes = 0,
            meshMessagesPending = 0,
            cpuHealth = 0.8,
            memoryUsage = 0.3,
            thermalHealth = 0.8,
            batteryLevel = 80,
            isAlive = isAlive
        )
    }
    
    /**
     * Interact with the organism
     * @param userInput User's input/query
     * @return AI response
     */
    suspend fun interact(userInput: String): String = withContext(Dispatchers.Default) {
        if (!isAlive) {
            return@withContext "Organism not initialized. Please start the system first."
        }
        
        try {
            Log.d(TAG, "Processing interaction: $userInput")
            
            // Retrieve context from RAG
            val context = ragEngine.retrieveContext(userInput, 3)
            val contextStr = context.joinToString("\n") { it.content }
            
            // Generate response via LLM
            val response = llmEngine.generateResponse(userInput, contextStr)
            
            // Make decision via Omega Arbiter
            val decision = omegaArbiter.makeDecision(
                userInput,
                JSONObject().apply {
                    put("response", response)
                    put("context", contextStr)
                }
            )
            
            response
        } catch (e: Exception) {
            Log.e(TAG, "Interaction error", e)
            "I apologize, but I encountered an error processing your request: ${e.message}"
        }
    }
    
    /**
     * Shutdown the organism
     */
    fun shutdown() {
        Log.i(TAG, "Shutting down VENOM Organism...")
        
        isAlive = false
        vitalsJob?.cancel()
        
        // Stop all components
        thetaMonitor.cleanup()
        llmEngine.cleanup()
        ragEngine.cleanup()
        omegaArbiter.cleanup()
        
        if (::bridge.isInitialized) {
            bridge.stopLambdaOrganism()
        }
        
        scope.cancel()
        
        Log.i(TAG, "VENOM Organism terminated")
    }
    // --- EXTENSII HIBRIDE ---
    /**
     * Monitorizare periodică a vitals (5s) + broadcast mesh
     */
    fun startAdvancedVitalsMonitoring() {
        scope.launch {
            while (isAlive) {
                try {
                    val vitals = getVitals()
                    logVitals(vitals)
                    // Broadcast către mesh
                    if (::bridge.isInitialized) {
                        bridge.broadcastToMesh(
                            "Vitals: θ=${"%.3f".format(vitals.theta)}, Λ=${"%.3f".format(vitals.lambdaScore)}"
                        )
                    }
                    delay(5000)
                } catch (e: Exception) {
                    Log.e(TAG, "Advanced vitals monitoring error: ${e.message}")
                }
            }
        }
    }

    /**
     * Logare extinsă a vitals
     */
    private fun logVitals(vitals: OrganismVitals) {
        Log.d(TAG, """
            💓 ORGANISM VITALS:
            ├─ Theta (θ): ${"%.3f".format(vitals.theta)}
            ├─ Lambda Score: ${"%.3f".format(vitals.lambdaScore)}
            ├─ Mesh Nodes: ${vitals.meshNodes}
            ├─ CPU Health: ${"%.1f%%".format(vitals.cpuHealth * 100)}
            ├─ Memory: ${"%.1f%%".format(vitals.memoryUsage * 100)}
            ├─ Thermal: ${"%.1f%%".format(vitals.thermalHealth * 100)}
            └─ Battery: ${vitals.batteryLevel}%
        """.trimIndent())
    }

    /**
     * Status detaliat organism
     */
    fun printOrganismStatus() {
        Log.i(TAG, """
            ═══════════════════════════════════════════════
              🌌 VENOM Ω-Λ ORGANISM: STATUS 🌌
            ═══════════════════════════════════════════════
            Ω COMPONENTS:
            ✅ Hardware Manager (Corp Digital)
            ✅ Theta Monitor (Metabolism)
            ✅ Möbius Engine (Time Compression)
            ✅ LLM Engine (Neural Network)
            ✅ RAG Engine (Knowledge)
            ✅ Omega Arbiter (Brain)
            Λ COMPONENTS:
            ✅ Lambda Arbiter (Nucleu)
            ✅ Organe [Optimize, Balance, Regenerate, Entropy]
            ✅ Pulse Fractal (Inima)
            ✅ Mesh Network (Țesuturi)
            ✅ NanoBots (Celule)
            Organismul respiră, gândește și evoluează...
        """.trimIndent())
    }

    /**
     * Shutdown robust cu logare extinsă
     */
    fun shutdownGracefully() {
        try {
            Log.i(TAG, "🛑 Shutting down organism gracefully...")
            isAlive = false
            vitalsJob?.cancel()
            thetaMonitor.cleanup()
            llmEngine.cleanup()
            ragEngine.cleanup()
            omegaArbiter.cleanup()
            if (::bridge.isInitialized) {
                bridge.stopLambdaOrganism()
            }
            scope.cancel()
            Log.i(TAG, "✅ Organism shutdown complete")
        } catch (e: Exception) {
            Log.e(TAG, "Graceful shutdown error: ${e.message}")
        }
    }
}
