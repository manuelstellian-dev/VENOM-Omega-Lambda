"""
Mesh Network - Țesuturi Digitale (Sânge + Nervi)
NanoBots communicate like neurons and blood cells
"""

import threading
import queue
import time
import logging
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO)

class Mesh:
    """
    Rețea Mesh - Țesuturi Digitale (Sânge + Nervi)
    NanoBots = Celule digitale care comunică
    """
    
    def __init__(self):
        self.nodes: Dict[str, Any] = {}  # NanoBots
        self.message_queue = queue.Queue()
        self.alive = False
        self.signal_log = []
        
        # Statistics
        self.messages_delivered = 0
        self.messages_dropped = 0
        self.total_nodes = 0
        
        logging.info("🕸️ Mesh Network initialized")
    
    def add_node(self, node_id: str, node_ref: Any):
        """
        Adaugă un NanoBot în mesh
        
        Args:
            node_id: Unique identifier for the node
            node_ref: NanoBot instance reference
        """
        self.nodes[node_id] = node_ref
        self.total_nodes += 1
        
        logging.info(f"🔗 Mesh: Added node {node_id} (total: {len(self.nodes)})")
    
    def remove_node(self, node_id: str):
        """
        Remove a NanoBot from mesh
        
        Args:
            node_id: Node identifier to remove
        """
        if node_id in self.nodes:
            del self.nodes[node_id]
            logging.info(f"🔗 Mesh: Removed node {node_id} (remaining: {len(self.nodes)})")
    
    def broadcast(self, sender: str, data: Any):
        """
        Broadcast mesaj la toate nodurile (ca sângele/nervii)
        
        Args:
            sender: Node ID of sender
            data: Data to broadcast
        """
        broadcast_count = 0
        
        for nid, ref in self.nodes.items():
            if nid != sender:  # Don't send back to sender
                try:
                    self.message_queue.put((nid, data), timeout=0.001)
                    broadcast_count += 1
                except queue.Full:
                    self.messages_dropped += 1
                    logging.warning(f"⚠️ Mesh: Message queue full, dropped message to {nid}")
        
        if broadcast_count > 0:
            logging.debug(f"📡 Mesh: Broadcast from {sender} to {broadcast_count} nodes")
    
    def send(self, recipient: str, data: Any):
        """
        Send message to specific node
        
        Args:
            recipient: Target node ID
            data: Data to send
        """
        if recipient in self.nodes:
            try:
                self.message_queue.put((recipient, data), timeout=0.001)
            except queue.Full:
                self.messages_dropped += 1
                logging.warning(f"⚠️ Mesh: Message queue full, dropped message to {recipient}")
    
    def deliver(self):
        """
        Loop de livrare mesaje (impulsuri nervoase)
        1ms delivery fractal
        """
        logging.info("🕸️ Mesh: Delivery loop started")
        
        while self.alive:
            try:
                # Non-blocking check for messages
                if not self.message_queue.empty():
                    nid, data = self.message_queue.get(timeout=0.001)
                    
                    if nid in self.nodes:
                        try:
                            # Deliver message (like neuron firing)
                            self.nodes[nid].receive(data)
                            
                            # Log signal
                            self.signal_log.append({
                                "timestamp": time.time(),
                                "recipient": nid,
                                "data": str(data)[:50]  # First 50 chars
                            })
                            
                            self.messages_delivered += 1
                            
                            # Keep only last 1000 signals
                            if len(self.signal_log) > 1000:
                                self.signal_log = self.signal_log[-1000:]
                                
                        except Exception as e:
                            logging.error(f"❌ Mesh: Delivery error to {nid}: {e}")
                            self.messages_dropped += 1
                
                # 1ms fractal delivery
                time.sleep(0.001)
                
            except queue.Empty:
                time.sleep(0.001)
            except Exception as e:
                logging.error(f"❌ Mesh: Delivery loop error: {e}")
                time.sleep(0.001)
    
    def start(self):
        """
        Pornește mesh-ul
        """
        if self.alive:
            logging.warning("🕸️ Mesh: Already running")
            return
        
        self.alive = True
        
        # Start delivery thread
        delivery_thread = threading.Thread(target=self.deliver, daemon=True)
        delivery_thread.start()
        
        logging.info(f"🕸️ Mesh Network: STARTED (nodes: {len(self.nodes)})")
    
    def stop(self):
        """
        Oprește mesh-ul
        """
        if not self.alive:
            logging.warning("🕸️ Mesh: Not running")
            return
        
        self.alive = False
        
        # Log final statistics
        logging.info(f"""
🕸️ Mesh Network: STOPPED
   - Total nodes: {self.total_nodes}
   - Messages delivered: {self.messages_delivered}
   - Messages dropped: {self.messages_dropped}
   - Signals logged: {len(self.signal_log)}
        """.strip())
    
    def get_vitals(self) -> Dict[str, Any]:
        """
        Obține semnale vitale din mesh
        
        Returns:
            Dict with mesh statistics
        """
        return {
            "alive": self.alive,
            "nodes": len(self.nodes),
            "messages_pending": self.message_queue.qsize(),
            "messages_delivered": self.messages_delivered,
            "messages_dropped": self.messages_dropped,
            "signals_logged": len(self.signal_log),
            "total_nodes_created": self.total_nodes
        }
    
    def get_node_states(self) -> Dict[str, Dict[str, Any]]:
        """
        Get state of all nodes
        
        Returns:
            Dict mapping node_id to node state
        """
        states = {}
        
        for nid, node in self.nodes.items():
            try:
                states[nid] = node.get_state()
            except Exception as e:
                logging.error(f"Error getting state for {nid}: {e}")
                states[nid] = {"error": str(e)}
        
        return states
    
    def get_recent_signals(self, count: int = 10) -> list:
        """
        Get recent signals from log
        
        Args:
            count: Number of recent signals to return
            
        Returns:
            List of recent signals
        """
        return self.signal_log[-count:]


def main():
    """
    Test Mesh Network
    """
    from nanobot import NanoBot
    
    logging.info("🕸️ Testing Mesh Network...")
    
    # Create mesh
    mesh = Mesh()
    mesh.start()
    
    # Add nanobots
    for i in range(1, 6):
        role = ["memory_carrier", "signal_relay", "knowledge_keeper"][i % 3]
        nanobot = NanoBot(f"nano_{i}", role)
        mesh.add_node(f"nano_{i}", nanobot)
    
    # Test broadcast
    mesh.broadcast("nano_1", "Test broadcast message from nano_1")
    
    # Wait for delivery
    time.sleep(0.1)
    
    # Test direct send
    mesh.send("nano_3", "Direct message to nano_3")
    
    # Wait for delivery
    time.sleep(0.1)
    
    # Get vitals
    vitals = mesh.get_vitals()
    logging.info(f"🕸️ Mesh vitals: {vitals}")
    
    # Get node states
    states = mesh.get_node_states()
    for nid, state in states.items():
        logging.info(f"   [{nid}]: {state}")
    
    # Stop mesh
    mesh.stop()
    
    logging.info("🕸️ Test completed")


if __name__ == "__main__":
    main()
