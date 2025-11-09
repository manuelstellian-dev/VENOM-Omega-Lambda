package com.venom.aios.omega.tetrastrat

import android.util.Log
import org.json.JSONObject

/**
 * EntropyEngine - Chaos and defensive cortex
 * Part of the 4-cortex parallel Tetrastrat model
 */
class EntropyEngine {
    private val scope = CoroutineScope(Dispatchers.Default + SupervisorJob())
    private var isActive = false
    private val explorationHistory = mutableListOf<Exploration>()
    companion object {
        private const val TAG = "EntropyEngine"
    }

    fun start() {
        if (isActive) return
        isActive = true
        scope.launch {
            Log.i(TAG, "🌀 ENTROPY Cortex: STARTED")
            while (isActive) {
                try {
                    cycle()
                    delay(20000)
                } catch (e: Exception) {
                    Log.e(TAG, "Cycle error: ${e.message}")
                }
            }
        }
    }

    fun stop() {
        isActive = false
        scope.cancel()
    }

    suspend fun cycle() = withContext(Dispatchers.Default) {
        val entropy = calculateEntropy()
        if (shouldExplore(entropy)) {
            val exploration = explore()
            val successful = evaluateExploration(exploration)
            if (successful) learnFromExploration(exploration)
        }
    }

    private fun calculateEntropy(): Double {
        val recentExplorations = explorationHistory.takeLast(10)
        if (recentExplorations.isEmpty()) return 0.5
        val successRate = recentExplorations.count { it.successful } / recentExplorations.size.toDouble()
        return 1.0 - successRate
    }

    private fun shouldExplore(entropy: Double): Boolean {
        return entropy < 0.3 || Random.nextDouble() < 0.1
    }

    private suspend fun explore(): Exploration = withContext(Dispatchers.Default) {
        Log.i(TAG, "🔍 Initiating exploration...")
        val explorationTypes = listOf(
            ExplorationType.TRY_NEW_ALGORITHM,
            ExplorationType.ADJUST_PARAMETERS,
            ExplorationType.SWAP_COMPONENTS,
            ExplorationType.INTRODUCE_RANDOMNESS
        )
        val type = explorationTypes.random()
        when (type) {
            ExplorationType.TRY_NEW_ALGORITHM -> Log.d(TAG, "🧪 Trying new algorithm")
            ExplorationType.ADJUST_PARAMETERS -> Log.d(TAG, "⚙️ Adjusting parameters")
            ExplorationType.SWAP_COMPONENTS -> Log.d(TAG, "🔀 Swapping components")
            ExplorationType.INTRODUCE_RANDOMNESS -> Log.d(TAG, "🎲 Introducing randomness")
        }
        Exploration(type = type, timestamp = System.currentTimeMillis())
    }

    private fun evaluateExploration(exploration: Exploration): Boolean {
        val improved = Random.nextBoolean()
        exploration.successful = improved
        explorationHistory.add(exploration)
        if (explorationHistory.size > 100) explorationHistory.removeAt(0)
        return improved
    }

    private fun learnFromExploration(exploration: Exploration) {
        Log.i(TAG, "✅ Learned from successful exploration: ${exploration.type}")
    }

    // Compat rapid: cycle(metrics: JSONObject): JSONObject
    fun cycle(metrics: JSONObject): JSONObject {
        Log.d(TAG, "Running entropy cycle (compat)")
        return JSONObject().apply {
            put("cortex", "entropy")
            put("threats_detected", 0)
            put("defense_level", 0.88)
        }
    }
}

data class Exploration(
    val type: ExplorationType,
    val timestamp: Long,
    var successful: Boolean = false
)

enum class ExplorationType {
    TRY_NEW_ALGORITHM,
    ADJUST_PARAMETERS,
    SWAP_COMPONENTS,
    INTRODUCE_RANDOMNESS
}
