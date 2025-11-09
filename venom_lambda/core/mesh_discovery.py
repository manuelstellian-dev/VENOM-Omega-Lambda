#!/usr/bin/env python3
# lambda/core/mesh_discovery.py

"""
mesh_discovery.py – VENOM Λ-Core Mesh Discovery Daemon
Folosește UDP Multicast pentru a anunța și descoperi nodurile VENOM
din rețeaua locală. Menține registrul de peer-uri (~/.venom_peers.json).
"""

import socket
import struct
import time
import json
import uuid
import threading
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s')

# --- Configurație Imutabilă ---
MULTICAST_GROUP = '224.1.1.1'
MULTICAST_PORT = 19845
TTL = 5                               # Time-To-Live pentru pachet
ANNOUNCEMENT_INTERVAL = 3.0           # Frecvența de anunțare (sec)
PEER_TIMEOUT = 10.0                   # Timp după care un peer e considerat mort
PEER_FILE = Path.home() / ".venom_peers.json"

# UUID-ul unic al acestui nod
NODE_ID = str(uuid.uuid4())

# Registru de Peer-uri în Memorie: {id: {"addr": (host, port), "last_seen": timestamp, "healthy": True}}
PEERS = {}

def load_peers():
    """Încarcă registrul de peer-uri de pe disc."""
    global PEERS
    if PEER_FILE.exists():
        try:
            PEERS = json.loads(PEER_FILE.read_text())
            # Convertim adresele la tuple
            for info in PEERS.values():
                if isinstance(info.get('addr'), list):
                    info['addr'] = tuple(info['addr'])
            logging.info(f"🕸️ Loaded {len(PEERS)} peers from {PEER_FILE}")
        except Exception as e:
            logging.error(f"Failed to load peers: {e}")
            PEERS = {}
    
def save_peers():
    """Salvează registrul de peer-uri pe disc (pentru Orchestrator)."""
    try:
        PEER_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        # Asigurăm că adresele sunt liste pentru serializare JSON
        serializable_peers = {}
        for pid, info in PEERS.items():
            serializable_info = info.copy()
            if isinstance(serializable_info.get('addr'), tuple):
                serializable_info['addr'] = list(serializable_info['addr'])
            serializable_peers[pid] = serializable_info
            
        PEER_FILE.write_text(json.dumps(serializable_peers, indent=4))
        logging.debug(f"💾 Saved {len(serializable_peers)} peers to {PEER_FILE}")
    except Exception as e:
        logging.error(f"Failed to save peers: {e}")

def announce_presence(sock):
    """Trimite un pachet Multicast pentru a anunța prezența."""
    try:
        # Presupunem că venom-api.py rulează pe portul 8000 (CFG.rest_port)
        message = json.dumps({
            "id": NODE_ID,
            "grpc_port": 8443,
            "rest_port": 8000,
            "timestamp": time.time()
        }).encode('utf-8')
        
        sock.sendto(message, (MULTICAST_GROUP, MULTICAST_PORT))
        
        # Adaugă nodul propriu în registru (pentru coerență)
        PEERS[NODE_ID] = {
            "addr": ('127.0.0.1', 8443),
            "last_seen": time.time(),
            "healthy": True,
            "is_local": True
        }
        
        logging.debug(f"📡 Announced presence: {NODE_ID[:8]}...")
    except Exception as e:
        logging.error(f"Announce error: {e}")

def listen_and_process(sock):
    """Ascultă pachetele Multicast și actualizează registrul."""
    sock.settimeout(ANNOUNCEMENT_INTERVAL) # Timeout pentru a permite loop-ul să curețe
    
    while True:
        try:
            data, address = sock.recvfrom(1024)
            message = json.loads(data.decode('utf-8'))
            
            peer_id = message.get("id")
            grpc_port = message.get("grpc_port", 8443)
            
            if peer_id == NODE_ID:
                continue # Ignoră propriul anunț
            
            peer_address = (address[0], grpc_port) # address[0] e IP-ul sursă
            
            # Actualizează sau adaugă peer-ul
            PEERS[peer_id] = {
                "addr": peer_address,
                "last_seen": time.time(),
                "healthy": PEERS.get(peer_id, {}).get("healthy", True),
                "is_local": False
            }
            
            logging.debug(f"🔗 Discovered peer: {peer_id[:8]}... at {peer_address}")
            
        except socket.timeout:
            pass
        except json.JSONDecodeError as e:
            logging.warning(f"Invalid JSON received: {e}")
        except Exception as e:
            logging.error(f"Listen error: {e}")

def cleanup_peers():
    """Curăță peer-urile care nu au mai anunțat de mult timp."""
    to_remove = []
    current_time = time.time()
    
    for peer_id, info in PEERS.items():
        if peer_id != NODE_ID and current_time - info['last_seen'] > PEER_TIMEOUT:
            to_remove.append(peer_id)
            
    for peer_id in to_remove:
        logging.info(f"🗑️ Removing stale peer: {peer_id[:8]}...")
        del PEERS[peer_id]

def multicast_daemon():
    """Funcția principală a Daemon-ului Multicast."""
    
    logging.info(f"🕸️ VENOM Mesh Discovery Daemon starting (ID: {NODE_ID[:8]}...)")
    
    # 1. Socket de trimis
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    send_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL)
    
    # 2. Socket de primit
    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    recv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind to multicast port
    try:
        recv_sock.bind(('', MULTICAST_PORT))
    except OSError as e:
        logging.error(f"Failed to bind to port {MULTICAST_PORT}: {e}")
        return

    # Join multicast group
    mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
    recv_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    logging.info(f"🕸️ Listening on {MULTICAST_GROUP}:{MULTICAST_PORT}")

    # 3. Start thread-ul de ascultare
    listen_thread = threading.Thread(target=lambda: listen_and_process(recv_sock), daemon=True)
    listen_thread.start()
    
    # 4. Loop-ul principal de anunțare și curățare
    last_save = 0
    try:
        while True:
            announce_presence(send_sock)
            cleanup_peers()
            
            # Salvează la fiecare 1 secundă
            if time.time() - last_save > 1:
                save_peers()
                last_save = time.time()
                
            time.sleep(ANNOUNCEMENT_INTERVAL)
    except KeyboardInterrupt:
        logging.info("\n🛑 Daemon stopped by user")
    except Exception as e:
        logging.error(f"Daemon error: {e}")
    finally:
        send_sock.close()
        recv_sock.close()

if __name__ == "__main__":
    load_peers()
    try:
        multicast_daemon()
    except Exception as e:
        logging.error(f"Fatal error: {e}")
