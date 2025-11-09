"""
NanoBot - Celulă Digitală
Păstrează memorie locală și procesează semnale (ca un neuron)
"""

import logging
import time
from typing import Any, Dict, List

logging.basicConfig(level=logging.INFO)

class NanoBot:
    """
    NanoBot - Celulă Digitală
    Păstrează memorie locală și procesează semnale
    Roles: memory_carrier, signal_relay, knowledge_keeper, generic
    """
    
    def __init__(self, node_id: str, role: str = "generic"):
        """
        Initialize NanoBot
        
        Args:
            node_id: Unique identifier
            role: NanoBot role (memory_carrier, signal_relay, knowledge_keeper, generic)
        """
        self.node_id = node_id
        self.role = role
        self.memory: List[Dict[str, Any]] = []
        self.active = True
        
        # Statistics
        self.messages_received = 0
        self.messages_processed = 0
        self.created_at = time.time()
        
        # Role-specific capacity
        self.memory_capacity = self._get_memory_capacity()
        
        logging.info(f"🤖 NanoBot {node_id} created (role: {role})")
    
    def _get_memory_capacity(self) -> int:
        """
        Get memory capacity based on role
        
        Returns:
            Maximum number of messages to store
        """
        capacities = {
            "memory_carrier": 200,      # High capacity for storing data
            "signal_relay": 50,          # Low capacity, fast relay
            "knowledge_keeper": 500,     # Very high capacity for knowledge
            "generic": 100               # Default capacity
        }
        
        return capacities.get(self.role, 100)
    
    def receive(self, data: Any):
        """
        Primește semnal (ca un neuron)
        
        Args:
            data: Received data
        """
        if not self.active:
            return
        
        self.messages_received += 1
        
        # Store message with metadata
        message = {
            "timestamp": time.time(),
            "data": data,
            "processed": False
        }
        
        self.memory.append(message)
        
        # Process based on role
        self._process_message(message)
        
        # Keep memory within capacity (FIFO eviction)
        if len(self.memory) > self.memory_capacity:
            evicted = self.memory.pop(0)
            logging.debug(f"🤖 [{self.node_id}] Evicted old message (capacity: {self.memory_capacity})")
        
        logging.debug(f"🤖 [{self.node_id}] Received: {str(data)[:50]}")
    
    def _process_message(self, message: Dict[str, Any]):
        """
        Process message based on role
        
        Args:
            message: Message to process
        """
        if self.role == "memory_carrier":
            # Store and index for fast retrieval
            message["indexed"] = True
            
        elif self.role == "signal_relay":
            # Fast relay - minimal processing
            message["relayed"] = True
            
        elif self.role == "knowledge_keeper":
            # Deep processing and indexing
            message["indexed"] = True
            message["processed"] = True
            
        elif self.role == "generic":
            # Basic processing
            message["processed"] = True
        
        self.messages_processed += 1
    
    def get_state(self) -> Dict[str, Any]:
        """
        Obține starea nanobot-ului
        
        Returns:
            Dict with nanobot state
        """
        uptime = time.time() - self.created_at
        
        return {
            "id": self.node_id,
            "role": self.role,
            "active": self.active,
            "memory_size": len(self.memory),
            "memory_capacity": self.memory_capacity,
            "memory_usage": len(self.memory) / self.memory_capacity,
            "messages_received": self.messages_received,
            "messages_processed": self.messages_processed,
            "uptime_seconds": uptime
        }
    
    def query_memory(self, filter_fn=None) -> List[Dict[str, Any]]:
        """
        Query stored memory
        
        Args:
            filter_fn: Optional filter function
            
        Returns:
            List of matching messages
        """
        if filter_fn is None:
            return self.memory.copy()
        
        return [msg for msg in self.memory if filter_fn(msg)]
    
    def clear_memory(self):
        """
        Clear all stored memory
        """
        cleared_count = len(self.memory)
        self.memory.clear()
        logging.info(f"🤖 [{self.node_id}] Memory cleared ({cleared_count} messages)")
    
    def deactivate(self):
        """
        Deactivate nanobot (apoptosis)
        """
        self.active = False
        logging.info(f"🤖 [{self.node_id}] Deactivated (apoptosis)")
    
    def reactivate(self):
        """
        Reactivate nanobot
        """
        self.active = True
        logging.info(f"🤖 [{self.node_id}] Reactivated")
    
    def __repr__(self) -> str:
        return f"NanoBot({self.node_id}, role={self.role}, memory={len(self.memory)}/{self.memory_capacity})"


def main():
    """
    Test NanoBot
    """
    logging.info("🤖 Testing NanoBot...")
    
    # Create nanobots with different roles
    roles = ["memory_carrier", "signal_relay", "knowledge_keeper", "generic"]
    
    nanobots = []
    for i, role in enumerate(roles, 1):
        nanobot = NanoBot(f"test_nano_{i}", role)
        nanobots.append(nanobot)
    
    # Send test messages
    for nanobot in nanobots:
        for j in range(5):
            nanobot.receive(f"Test message {j} for {nanobot.node_id}")
    
    # Get states
    logging.info("\n🤖 NanoBot States:")
    for nanobot in nanobots:
        state = nanobot.get_state()
        logging.info(f"   {nanobot}")
        logging.info(f"      Usage: {state['memory_usage']:.1%}")
        logging.info(f"      Processed: {state['messages_processed']}")
    
    # Test memory query
    memory_carrier = nanobots[0]
    recent_messages = memory_carrier.query_memory(
        lambda msg: msg["timestamp"] > time.time() - 10
    )
    logging.info(f"\n🤖 Recent messages in {memory_carrier.node_id}: {len(recent_messages)}")
    
    # Test deactivation
    nanobots[1].deactivate()
    nanobots[1].receive("This should not be stored")
    logging.info(f"\n🤖 Deactivated nanobot memory: {len(nanobots[1].memory)}")
    
    logging.info("\n🤖 Test completed")


if __name__ == "__main__":
    main()
