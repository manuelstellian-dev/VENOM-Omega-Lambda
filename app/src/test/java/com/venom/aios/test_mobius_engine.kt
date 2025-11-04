package com.venom.aios

import com.venom.aios.omega.brain.AdaptiveMobiusEngine
import org.junit.Test
import org.junit.Assert.*

class AdaptiveMobiusEngineTest {
    
    @Test
    fun testCalculateTheta() {
        val engine = AdaptiveMobiusEngine()
        
        val theta = engine.calculateTheta(0.8, 0.7, 0.9)
        
        assertTrue(theta >= 0.0)
        assertTrue(theta <= 1.0)
        
        // Verify formula: 0.3*0.8 + 0.3*0.7 + 0.4*0.9
        val expected = 0.3 * 0.8 + 0.3 * 0.7 + 0.4 * 0.9
        assertEquals(expected, theta, 0.001)
    }
    
    @Test
    fun testAmdahlSpeedup() {
        val engine = AdaptiveMobiusEngine()
        
        val speedup = engine.amdahlSpeedup(4, 0.75)
        
        // Speedup should be > 1.0
        assertTrue(speedup > 1.0)
        
        // With 4 cores and 75% parallel, should be significant
        assertTrue(speedup < 4.0) // Can't exceed core count
    }
    
    @Test
    fun testCompressTime() {
        val engine = AdaptiveMobiusEngine()
        
        val original = 1000L
        val compressed = engine.compressTime(original, 0.7, 150.0)
        
        // Compressed time should be less than original
        assertTrue(compressed < original)
        assertTrue(compressed > 0)
    }
}
