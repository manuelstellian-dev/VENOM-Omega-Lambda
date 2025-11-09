"""
Mesh Orchestrator Service
Coordinates task distribution across mesh nodes
"""

import logging
import json
import time
import signal
import sys
from pathlib import Path
from typing import Dict, List, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PEERS_FILE = Path.home() / '.venom_peers.json'


class MeshOrchestrator:
    """Orchestrates work across mesh nodes"""
    
    def __init__(self):
        self.peers = {}
        self.load_tracking: Dict[str, float] = {}
        self.running = False
        
    def load_peers(self):
        """Load peers from discovery file"""
        try:
            if PEERS_FILE.exists():
                with open(PEERS_FILE, 'r') as f:
                    self.peers = json.load(f)
                logger.info(f"Loaded {len(self.peers)} peers")
        except Exception as e:
            logger.error(f"Failed to load peers: {e}")
    
    def health_check(self, node_id: str) -> bool:
        """Check if node is healthy"""
        if node_id not in self.peers:
            return False
        
        last_seen = self.peers[node_id].get('last_seen', 0)
        return (time.time() - last_seen) < 60  # 1 minute threshold
    
    def dispatch_task(self, task: Dict[str, Any]) -> str:
        """
        Dispatch task to least loaded node
        
        Returns:
            Node ID where task was dispatched
        """
        # Find least loaded healthy node
        candidates = [
            node_id for node_id in self.peers.keys()
            if self.health_check(node_id)
        ]
        
        if not candidates:
            logger.warning("No healthy nodes available")
            return None
        
        # Select node with lowest load
        selected = min(candidates, key=lambda n: self.recent_load(n))
        
        # Update load tracking (using EMA)
        self.load_tracking[selected] = self.recent_load(selected) * 0.9 + 1.0
        
        logger.info(f"Dispatched task to {selected}")
        return selected
    
    def recent_load(self, node_id: str) -> float:
        """Get recent load for node (EMA)"""
        return self.load_tracking.get(node_id, 0.0)
    
    def orchestrator_loop(self):
        """Main orchestration loop"""
        self.running = True
        
        while self.running:
            try:
                # Reload peers periodically
                self.load_peers()
                
                # Decay load tracking
                for node_id in list(self.load_tracking.keys()):
                    self.load_tracking[node_id] *= 0.95
                
                time.sleep(10)
                
            except Exception as e:
                logger.error(f"Orchestrator error: {e}")
    
    def stop(self):
        """Stop orchestrator"""
        self.running = False
        logger.info("Orchestrator stopped")


def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logger.info("Shutting down...")
    sys.exit(0)


def main():
    """Main entry point"""
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    orchestrator = MeshOrchestrator()
    orchestrator.orchestrator_loop()


if __name__ == "__main__":
    main()

__all__ = ["MeshOrchestrator", "PEERS_FILE"]
