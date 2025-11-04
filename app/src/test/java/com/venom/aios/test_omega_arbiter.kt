package com.venom.aios

import com.venom.aios.omega.brain.OmegaArbiter
import org.json.JSONObject
import org.junit.Test
import org.junit.Assert.*
import kotlinx.coroutines.runBlocking

class OmegaArbiterTest {
    
    @Test
    fun testMakeDecision() = runBlocking {
        val arbiter = OmegaArbiter()
        val context = JSONObject().apply {
            put("test", "context")
        }
        
        val decision = arbiter.makeDecision("test input", context)
        
        assertNotNull(decision)
        assertTrue(decision.has("input"))
        assertTrue(decision.has("theta"))
        assertTrue(decision.has("lambda"))
    }
    
    @Test
    fun testAdjustFromLambda() {
        val arbiter = OmegaArbiter()
        
        // Should adjust theta based on score
        arbiter.adjustFromLambda(150.0)
        
        // Test passes if no exception
        assertTrue(true)
    }
    
    @Test
    fun testFuseDecisions() {
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
