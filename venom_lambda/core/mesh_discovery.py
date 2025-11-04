"""
Mesh Discovery Service
UDP multicast discovery for VENOM mesh nodes
"""

import logging
import socket
import json
import time
import signal
import sys
from pathlib import Path
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MULTICAST_GROUP = '224.1.1.1'
MULTICAST_PORT = 19845
PEERS_FILE = Path.home() / '.venom_peers.json'


class MeshDiscovery:
    """UDP multicast discovery service"""
    
    def __init__(self, node_id: str = None):
        self.node_id = node_id or f"venom-{int(time.time())}"
        self.peers: Dict[str, Dict[str, Any]] = {}
        self.running = False
        self.sock = None
        
    def announce_presence(self):
        """Announce this node's presence"""
        message = {
            "type": "announce",
            "node_id": self.node_id,
            "timestamp": int(time.time()),
            "capabilities": ["fractal", "arbiter", "mesh"]
        }
        
        data = json.dumps(message).encode('utf-8')
        
        # Send multicast
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        
        try:
            sock.sendto(data, (MULTICAST_GROUP, MULTICAST_PORT))
            logger.debug(f"Announced presence: {self.node_id}")
        except Exception as e:
            logger.error(f"Failed to announce: {e}")
        finally:
            sock.close()
    
    def listen_and_process(self):
        """Listen for announcements from other nodes"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.sock.bind(('', MULTICAST_PORT))
        
        mreq = socket.inet_aton(MULTICAST_GROUP) + socket.inet_aton('0.0.0.0')
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        
        logger.info(f"Listening on {MULTICAST_GROUP}:{MULTICAST_PORT}")
        
        self.running = True
        while self.running:
            try:
                data, addr = self.sock.recvfrom(1024)
                message = json.loads(data.decode('utf-8'))
                
                if message['node_id'] != self.node_id:
                    self.peers[message['node_id']] = {
                        "address": addr[0],
                        "last_seen": int(time.time()),
                        "capabilities": message.get('capabilities', [])
                    }
                    logger.info(f"Discovered peer: {message['node_id']} at {addr[0]}")
                    self.save_peers()
                    
            except socket.timeout:
                continue
            except Exception as e:
                logger.error(f"Error processing message: {e}")
    
    def cleanup_peers(self):
        """Remove stale peers"""
        now = int(time.time())
        stale = [
            node_id for node_id, info in self.peers.items()
            if now - info['last_seen'] > 300  # 5 minutes
        ]
        for node_id in stale:
            del self.peers[node_id]
            logger.info(f"Removed stale peer: {node_id}")
    
    def save_peers(self):
        """Save peers to file"""
        try:
            with open(PEERS_FILE, 'w') as f:
                json.dump(self.peers, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save peers: {e}")
    
    def stop(self):
        """Stop discovery service"""
        self.running = False
        if self.sock:
            self.sock.close()
        logger.info("Discovery service stopped")


def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logger.info("Shutting down...")
    sys.exit(0)


def main():
    """Main entry point"""
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    discovery = MeshDiscovery()
    
    # Announce periodically
    import threading
    def announce_loop():
        while True:
            discovery.announce_presence()
            time.sleep(30)
    
    announce_thread = threading.Thread(target=announce_loop, daemon=True)
    announce_thread.start()
    
    # Listen for peers
    discovery.listen_and_process()


if __name__ == "__main__":
    main()
