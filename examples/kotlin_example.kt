// Example: VENOM Organism Lifecycle and Interaction
// This demonstrates basic usage of the VENOM system

import com.venom.aios.main.VenomOrganism
import android.content.Context
import kotlinx.coroutines.runBlocking

fun demonstrateVenomUsage(context: Context) {
    // Get singleton instance
    val organism = VenomOrganism.getInstance(context)
    
    runBlocking {
        // Birth the organism
        println("🌱 Initiating VENOM organism birth...")
        val birthSuccess = organism.birth()
        
        if (!birthSuccess) {
            println("❌ Failed to initialize organism")
            return@runBlocking
        }
        
        println("✅ Organism is alive!")
        
        // Start vitals monitoring
        organism.startVitalsMonitoring { vitals ->
            println("""
                === System Vitals ===
                Theta (θ): ${vitals.theta}
                Lambda (Λ): ${vitals.lambdaScore}
                Mesh Nodes: ${vitals.meshNodes}
                CPU Health: ${vitals.cpuHealth * 100}%
                Memory Usage: ${vitals.memoryUsage * 100}%
                Status: ${if (vitals.isAlive) "ALIVE" else "DEAD"}
            """.trimIndent())
        }
        
        // Interact with the organism
        println("\n💬 Interacting with VENOM...")
        val queries = listOf(
            "What is VENOM?",
            "Explain theta compression",
            "How does the mesh network work?"
        )
        
        for (query in queries) {
            println("\nUser: $query")
            val response = organism.interact(query)
            println("VENOM: $response")
        }
        
        // Get current vitals
        val vitals = organism.getVitals()
        println("\nFinal vitals: $vitals")
        
        // Shutdown
        println("\n🛑 Shutting down organism...")
        organism.shutdown()
        println("✅ Shutdown complete")
    }
}
