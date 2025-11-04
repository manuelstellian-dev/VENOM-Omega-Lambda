package com.venom.aios

import android.content.Context
import androidx.test.core.app.ApplicationProvider
import androidx.test.ext.junit.runners.AndroidJUnit4
import com.venom.aios.omega.brain.ThetaMonitor
import org.junit.Test
import org.junit.Assert.*
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class ThetaMonitorTest {
    
    @Test
    fun testCalculateTheta() {
        val context = ApplicationProvider.getApplicationContext<Context>()
        val monitor = ThetaMonitor(context)
        
        val theta = monitor.calculateTheta()
        
        assertTrue(theta >= 0.0)
        assertTrue(theta <= 1.0)
    }
    
    @Test
    fun testGetCPUHealth() {
        val context = ApplicationProvider.getApplicationContext<Context>()
        val monitor = ThetaMonitor(context)
        
        val cpuHealth = monitor.getCPUHealth()
        
        assertTrue(cpuHealth >= 0.0)
        assertTrue(cpuHealth <= 1.0)
    }
}
