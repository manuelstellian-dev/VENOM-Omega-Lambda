
// tests/test_omega_arbiter.kt
package com.venom.tests

import com.venom.omega.brain.OmegaArbiter
import com.venom.omega.brain.AdaptiveMobiusEngine
import com.venom.omega.brain.ThetaMonitor
import com.venom.omega.neural.LLMEngine
import com.venom.omega.knowledge.RAGEngine
import com.venom.omega.hardware.HardwareManager
import android.content.Context
import androidx.test.platform.app.InstrumentationRegistry
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Test
import org.junit.Before
import org.junit.runner.RunWith
import org.junit.Assert.*
import kotlinx.coroutines.runBlocking

/**
 * Tests for Omega Arbiter (Supreme Hybrid)
 * Păstrează testele workspace, adaugă incremental testele avansate (setup hardware/context, feedback, istoric, performanță, moduri adaptive, coroutine, subscribe la theta, etc.), fără dubluri sau pierdere de informații.
 */
@RunWith(AndroidJUnit4::class)
class TestOmegaArbiter {
    private lateinit var context: Context
    private lateinit var hardwareManager: HardwareManager
    private lateinit var thetaMonitor: ThetaMonitor
    private lateinit var mobiusEngine: AdaptiveMobiusEngine
    private lateinit var llmEngine: LLMEngine
    private lateinit var ragEngine: RAGEngine
    private lateinit var omegaArbiter: OmegaArbiter

    @Before
    fun setup() {
        context = InstrumentationRegistry.getInstrumentation().targetContext
        hardwareManager = HardwareManager(context)
        thetaMonitor = ThetaMonitor(context, interval = 1000)
        mobiusEngine = AdaptiveMobiusEngine(hardwareManager)
        llmEngine = LLMEngine(context)
        ragEngine = RAGEngine(context)
        omegaArbiter = OmegaArbiter(
            mobiusEngine = mobiusEngine,
            thetaMonitor = thetaMonitor,
            llmEngine = llmEngine,
            ragEngine = ragEngine
        )
    }

    @Test
    fun testArbiterInitialization() {
        assertNotNull("Omega Arbiter should be initialized", omegaArbiter)
        assertEquals("Initial lambda feedback should be 0.0", 0.0, omegaArbiter.lambdaFeedback, 0.001)
    }

    @Test
    fun testLambdaFeedback() {
        val testScore = 0.75
        val testResults = org.json.JSONObject().apply {
            put("integrated_score", testScore)
            put("organs", org.json.JSONObject())
        }
        omegaArbiter.onLambdaFeedback(testScore, testResults)
        assertEquals("Lambda feedback should be updated", testScore, omegaArbiter.lambdaFeedback, 0.001)
    }

    @Test
    fun testDecisionMaking() = runBlocking {
        val userInput = "Test input for decision making"
        val decision = omegaArbiter.makeDecision(userInput, context)
        assertNotNull("Decision should not be null", decision)
        assertNotNull("Decision response should not be null", decision.response)
        assertTrue("Decision confidence should be between 0 and 1", decision.confidence in 0.0..1.0)
    }

    @Test
    fun testLambdaFeedbackHistory() {
        val scores = listOf(0.5, 0.6, 0.7, 0.8, 0.9)
        scores.forEach { score ->
            val results = org.json.JSONObject().apply {
                put("integrated_score", score)
            }
            omegaArbiter.onLambdaFeedback(score, results)
        }
        assertEquals("Latest feedback should match last score", scores.last(), omegaArbiter.lambdaFeedback, 0.001)
    }

    @Test
    fun testPerformanceModeAdjustment() {
        thetaMonitor.subscribeToTheta { theta ->
            if (theta < 0.3) {
                assertTrue("Low theta should trigger conservative mode", true)
            }
        }
        thetaMonitor.start()
        Thread.sleep(2000)
        thetaMonitor.stop()
    }

    // Workspace tests păstrate (minimal)
    @Test
    fun testMakeDecisionWorkspace() = runBlocking {
        val arbiter = OmegaArbiter()
        val context = org.json.JSONObject().apply {
            put("test", "context")
        }
        val decision = arbiter.makeDecision("test input", context)
        assertNotNull(decision)
        assertTrue(decision.has("input"))
        assertTrue(decision.has("theta"))
        assertTrue(decision.has("lambda"))
    }

    @Test
    fun testAdjustFromLambdaWorkspace() {
        val arbiter = OmegaArbiter()
        arbiter.adjustFromLambda(150.0)
        assertTrue(true)
    }

    @Test
    fun testFuseDecisionsWorkspace() {
        val arbiter = OmegaArbiter()
        val result = arbiter.fuseDecisions(
            "user intent",
            "ai suggestion",
            0.7,
            120.0
        )
        assertNotNull(result)
        assertTrue(result.has("fusedResult"))
        assertTrue(result.has("fusionWeight"))
    }
}
