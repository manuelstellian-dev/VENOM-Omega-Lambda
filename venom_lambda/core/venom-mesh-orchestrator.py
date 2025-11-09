#!/usr/bin/env python3
# lambda/core/venom-mesh-orchestrator.py

"""
VENOM Λ-Core mesh orchestrator.
- Citește registry de peers generat de mesh_discovery.py (~/.venom_peers.json).
- Face health-check periodic prin gRPC.
- Alege cel mai sănătos nod și face dispatch de taskuri Λ.
"""

import asyncio
import json
import time
import uuid
from pathlib import Path
from typing import Any, Dict
import logging

# gRPC imports (requires generated venom_pb2 and venom_pb2_grpc)
try:
    import grpc
    # Uncomment after generating proto:
    # import venom_pb2, venom_pb2_grpc
    GRPC_AVAILABLE = True
except ImportError:
    GRPC_AVAILABLE = False
    logging.warning("gRPC not available, orchestrator will not function")

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s')

PEER_FILE = Path.home() / ".venom_peers.json"
HEALTH_INTERVAL = 5.0

# Structura registry în memorie
PEERS: Dict[str, Dict[str, Any]] = {}

# --------------------------------------------------------------
# Utilities
def load_peers():
    """Încarcă registrul de peer-uri de pe disc."""
    global PEERS
    if PEER_FILE.exists():
        try:
            PEERS = json.loads(PEER_FILE.read_text())
            logging.info(f"📚 Loaded {len(PEERS)} peers from registry")
        except Exception as e:
            logging.error(f"Failed to load peers: {e}")
            PEERS = {}
    else:
        PEERS = {}
        logging.warning(f"Peer registry not found at {PEER_FILE}")

def recent_load(peer_id: str) -> float:
    """Simplu placeholder: contează câte requesturi active are nodul."""
    info = PEERS.get(peer_id, {})
    return info.get("inflight", 0.0)

# --------------------------------------------------------------
# Health check
async def health_check(peer_id: str, info: Dict[str, Any]):
    """
    Health check prin gRPC ping
    
    Args:
        peer_id: Peer identifier
        info: Peer information dict
    """
    if not GRPC_AVAILABLE:
        info["healthy"] = False
        return
    
    try:
        addr_tuple = info.get('addr', ('127.0.0.1', 8443))
        if isinstance(addr_tuple, list):
            addr_tuple = tuple(addr_tuple)
        
        addr = f"{addr_tuple[0]}:{addr_tuple[1]}"
        
        # Uncomment after generating proto:
        # async with grpc.aio.insecure_channel(addr) as channel:
        #     stub = venom_pb2_grpc.VenomStub(channel)
        #     # Simple health check via TimeWrap
        #     await stub.TimeWrap(venom_pb2.TimeWrapReq(k=100, p=10, u=1e6))
        
        info["healthy"] = True
        logging.debug(f"✅ Health check passed: {peer_id[:8]}...")
        
    except Exception as e:
        info["healthy"] = False
        logging.warning(f"❌ Health check failed for {peer_id[:8]}...: {e}")

# --------------------------------------------------------------
# Dispatcher
async def dispatch_task(task: Dict[str, Any]) -> Any:
    """
    Dispatch task to best available peer
    
    Args:
        task: Task dictionary with func, args, deadline
        
    Returns:
        Task result
    
    Example task:
        {
          "func": "fractal_total",
          "args": {"s": 1, "theta": 0.42},
          "deadline": time.time() + 10
        }
    """
    if not GRPC_AVAILABLE:
        raise RuntimeError("gRPC not available")
    
    load_peers()
    candidates = [(pid, info) for pid, info in PEERS.items() if info.get("healthy")]
    
    if not candidates:
        raise RuntimeError("No healthy peers available")

    # Pick peer with lowest load
    target_id, target_info = min(candidates, key=lambda x: recent_load(x[0]))
    
    addr_tuple = target_info.get('addr', ('127.0.0.1', 8443))
    if isinstance(addr_tuple, list):
        addr_tuple = tuple(addr_tuple)
    addr = f"{addr_tuple[0]}:{addr_tuple[1]}"
    
    logging.info(f"🎯 Dispatching task to {target_id[:8]}... at {addr}")

    # Uncomment after generating proto:
    # async with grpc.aio.insecure_channel(addr) as channel:
    #     stub = venom_pb2_grpc.VenomStub(channel)
    #     
    #     if task["func"] == "fractal_total":
    #         req = venom_pb2.FractalReq(
    #             s=task["args"]["s"],
    #             theta=task["args"]["theta"]
    #         )
    #         return await stub.FractalTotal(req, timeout=task.get("deadline"))
    #     
    #     elif task["func"] == "time_wrap":
    #         req = venom_pb2.TimeWrapReq(**task["args"])
    #         return await stub.TimeWrap(req, timeout=task.get("deadline"))
    #     
    #     # Add other functions as needed
    #     else:
    #         raise ValueError(f"Unknown function: {task['func']}")
    
    # Placeholder return
    return {"result": "simulated", "peer": target_id[:8]}

# --------------------------------------------------------------
# Main loop
async def orchestrator_loop():
    """Main orchestrator loop - health checks every HEALTH_INTERVAL"""
    logging.info("🎼 Orchestrator loop started")
    
    while True:
        load_peers()
        
        # Health check all peers
        checks = [health_check(pid, info) for pid, info in PEERS.items()]
        if checks:
            await asyncio.gather(*checks)
            logging.info(f"💓 Health checked {len(checks)} peers")
        
        await asyncio.sleep(HEALTH_INTERVAL)

# --------------------------------------------------------------
# Example run (test)
async def example():
    """Example task dispatch"""
    await asyncio.sleep(2)  # Wait for health init
    
    task = {
        "func": "time_wrap",
        "args": {"k": 120.0, "p": 8.0, "u": 2e6},
        "deadline": time.time() + 5
    }
    
    try:
        resp = await dispatch_task(task)
        logging.info(f"📊 Task result: {resp}")
    except Exception as e:
        logging.error(f"Task dispatch failed: {e}")

# --------------------------------------------------------------
if __name__ == "__main__":
    logging.info("🎼 VENOM Mesh Orchestrator starting...")
    
    loop = asyncio.get_event_loop()
    
    # Start orchestrator loop
    loop.create_task(orchestrator_loop())
    
    # Run example task
    loop.run_until_complete(example())
    
    # Keep running
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info("\n🛑 Orchestrator stopped by user")