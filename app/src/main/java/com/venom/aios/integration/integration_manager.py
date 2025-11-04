"""
Integration Manager - Python side coordinator
Interfaces with Android bridge layer
"""

import logging
from venom_lambda.arbiter_core import LambdaArbiter
from venom_lambda.pulse import PulseFractal
from venom_lambda.mesh import Mesh

logger = logging.getLogger(__name__)


class IntegrationManager:
    """Manages Python-side integration with Android"""
    
    def __init__(self):
        self.arbiter = LambdaArbiter()
        self.mesh = Mesh()
        self.pulse = None
        logger.info("IntegrationManager initialized")
    
    def start_organism(self, nanobot_count=10):
        """Start the Lambda organism"""
        logger.info(f"Starting Lambda organism with {nanobot_count} nanobots")
        
        # Populate mesh
        for i in range(nanobot_count):
            role = ["memory_carrier", "signal_relay", "knowledge_keeper", "generic"][i % 4]
            self.mesh.add_node(f"nanobot-{i}", role)
        
        # Start pulse
        self.pulse = PulseFractal(self.arbiter)
        
        return {
            "status": "started",
            "nanobots": nanobot_count,
            "mesh_nodes": len(self.mesh.nodes)
        }
    
    def process_health(self, health_data):
        """Process health data from Omega"""
        result = self.arbiter.time_wrap(health_data)
        return result
    
    def get_mesh_vitals(self):
        """Get mesh network vitals"""
        return self.mesh.get_vitals()
    
    def broadcast(self, message):
        """Broadcast message to mesh"""
        self.mesh.broadcast("android-bridge", message)
    
    def stop_organism(self):
        """Stop the organism"""
        logger.info("Stopping Lambda organism")
        return {"status": "stopped"}


# Global instance for Chaquopy access
_manager = None


def get_manager():
    """Get or create manager instance"""
    global _manager
    if _manager is None:
        _manager = IntegrationManager()
    return _manager
