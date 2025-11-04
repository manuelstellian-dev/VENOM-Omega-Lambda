"""
NanoBot - Individual mesh network node
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class NanoBot:
    """
    NanoBot - Individual node in the mesh network
    Roles: memory_carrier, signal_relay, knowledge_keeper, generic
    """
    
    VALID_ROLES = ["memory_carrier", "signal_relay", "knowledge_keeper", "generic"]
    
    def __init__(self, node_id: str, role: str = "generic"):
        """
        Initialize NanoBot
        
        Args:
            node_id: Unique identifier for this bot
            role: Bot's role in the mesh
        """
        if role not in self.VALID_ROLES:
            logger.warning(f"Invalid role {role}, using 'generic'")
            role = "generic"
        
        self.node_id = node_id
        self.role = role
        self.messages_received = []
        self.state = {
            "active": True,
            "load": 0.0,
            "memory_usage": 0.0
        }
        
        logger.debug(f"NanoBot {node_id} created (role={role})")
    
    def receive(self, data: Dict[str, Any]):
        """
        Receive a message
        
        Args:
            data: Message data
        """
        self.messages_received.append(data)
        
        # Role-specific processing
        if self.role == "memory_carrier":
            self._process_memory(data)
        elif self.role == "signal_relay":
            self._relay_signal(data)
        elif self.role == "knowledge_keeper":
            self._store_knowledge(data)
        else:
            self._generic_process(data)
        
        logger.debug(f"NanoBot {self.node_id} received message")
    
    def _process_memory(self, data: Dict[str, Any]):
        """Process data as memory carrier"""
        self.state["memory_usage"] += 0.01
    
    def _relay_signal(self, data: Dict[str, Any]):
        """Relay signal to other nodes"""
        self.state["load"] += 0.005
    
    def _store_knowledge(self, data: Dict[str, Any]):
        """Store knowledge data"""
        self.state["memory_usage"] += 0.02
    
    def _generic_process(self, data: Dict[str, Any]):
        """Generic processing"""
        self.state["load"] += 0.01
    
    def get_state(self) -> Dict[str, Any]:
        """Get bot state"""
        return {
            "node_id": self.node_id,
            "role": self.role,
            "messages_received": len(self.messages_received),
            **self.state
        }
