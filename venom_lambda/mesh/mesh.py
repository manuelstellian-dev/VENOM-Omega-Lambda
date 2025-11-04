"""
Mesh Network - Distributed communication and coordination
"""

import logging
import asyncio
from typing import Dict, List, Any
from .nanobot import NanoBot

logger = logging.getLogger(__name__)


class Mesh:
    """
    Mesh Network for multi-device/multi-process communication
    """
    
    def __init__(self):
        self.nodes: Dict[str, NanoBot] = {}
        self.messages: List[Dict[str, Any]] = []
        self.is_running = False
        
        logger.info("Mesh network initialized")
    
    def add_node(self, node_id: str, role: str = "generic") -> NanoBot:
        """
        Add a node to the mesh
        
        Args:
            node_id: Unique node identifier
            role: Node role (memory_carrier, signal_relay, knowledge_keeper, generic)
            
        Returns:
            Created NanoBot instance
        """
        if node_id in self.nodes:
            logger.warning(f"Node {node_id} already exists")
            return self.nodes[node_id]
        
        nanobot = NanoBot(node_id, role)
        self.nodes[node_id] = nanobot
        
        logger.info(f"Node added: {node_id} (role={role})")
        return nanobot
    
    def broadcast(self, sender: str, data: Dict[str, Any]):
        """
        Broadcast message to all nodes
        
        Args:
            sender: ID of sending node
            data: Message data
        """
        message = {
            "sender": sender,
            "data": data,
            "timestamp": self._get_timestamp()
        }
        
        self.messages.append(message)
        
        # Deliver to all nodes except sender
        for node_id, node in self.nodes.items():
            if node_id != sender:
                node.receive(data)
        
        logger.debug(f"Broadcast from {sender} to {len(self.nodes) - 1} nodes")
    
    def deliver(self, recipient: str, sender: str, data: Dict[str, Any]):
        """
        Deliver message to specific node
        
        Args:
            recipient: ID of receiving node
            sender: ID of sending node
            data: Message data
        """
        if recipient not in self.nodes:
            logger.warning(f"Recipient {recipient} not found")
            return
        
        self.nodes[recipient].receive(data)
        logger.debug(f"Message delivered: {sender} -> {recipient}")
    
    async def start(self):
        """Start the mesh network"""
        self.is_running = True
        logger.info("Mesh network started")
    
    async def stop(self):
        """Stop the mesh network"""
        self.is_running = False
        logger.info("Mesh network stopped")
    
    def get_vitals(self) -> Dict[str, Any]:
        """Get mesh network vitals"""
        return {
            "nodes": len(self.nodes),
            "messages": len(self.messages),
            "running": self.is_running,
            "node_roles": {
                node_id: node.role 
                for node_id, node in self.nodes.items()
            }
        }
    
    def _get_timestamp(self) -> int:
        """Get current timestamp in milliseconds"""
        import time
        return int(time.time() * 1000)
