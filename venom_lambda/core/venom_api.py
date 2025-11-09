#!/usr/bin/env python3
# lambda/core/venom-api.py

"""
venom-api.py – VENOM Λ-Core API (REST + gRPC local)
Exposes Lambda functions via FastAPI (REST) and gRPC
"""

import math
import os
import asyncio
from typing import List, Tuple
from dataclasses import dataclass
from pathlib import Path

from fastapi import FastAPI
import uvicorn

# Import gRPC (will be used after proto generation)
try:
    import grpc
    from concurrent import futures
    # These will be generated from venom.proto
    # import venom_pb2
    # import venom_pb2_grpc
    GRPC_AVAILABLE = True
except ImportError:
    GRPC_AVAILABLE = False
    print("[WARNING] gRPC not available, only REST will work")

# ======================================================
# Config centralizat
# ======================================================

@dataclass(frozen=True)
class Config:
    t1: float = 1.0
    k: float = 100.0
    p: float = 10.0
    u: float = 1e6
    theta_low: float = 0.3
    theta_high: float = 0.7
    grpc_port: int = 8443
    rest_port: int = 8000

CFG = Config()
VENOM_HOME = Path(os.getenv("VENOM_HOME", Path.home() / "venom"))

# ======================================================
# Funcții Λ (identice cu fractal.py)
# ======================================================

def time_wrap(k: float, p: float, u: float, t1: float = CFG.t1) -> float:
    """Λ‑TimeWrap"""
    if k * p == 1:
        raise ValueError("k * p must not equal 1")
    return (t1 * math.log(u)) / (1 - 1 / (k * p))

_STATE_MAP = {
    1: ("Regen", ["Scan","Detect","Quarantine","Heal","Improve","Reinvest"]),
    0: ("Neutral", ["Scan","Detect","Quarantine","Heal","Neutralize","Stabilize"]),
    -1: ("Entropy", ["Reinvest_neg","Degrade","Infect","Spread","Ignore","Blind"])
}

def fallback(theta: float) -> Tuple[str, List[str]]:
    """Λ‑Fallback"""
    if theta >= CFG.theta_high: return "Fallback→+1", ["Regen"]
    if theta >= CFG.theta_low: return "Fallback→0", ["Neutral"]
    return "Fallback→-1", ["Entropy"]

def fractal_total(s: float, theta: float) -> Tuple[str, List[str]]:
    """Λ‑Fractal Tetrastrat"""
    s_int = int(s) if s != float("inf") else float("inf")
    if s_int in _STATE_MAP: return _STATE_MAP[s_int]
    if s_int == float("inf"): return fallback(theta)
    raise ValueError("invalid state")

def mobius_time(s: float, k: float, p: float, u: float, theta: float, t1: float=CFG.t1) -> float:
    """Λ‑Möbius Temporal"""
    s_int = int(s) if s != float("inf") else float("inf")
    if s_int == 1: return time_wrap(k,p,u,t1)
    if s_int == 0: return t1 * math.log(u)
    if s_int == -1: return sum(t1*((k*p)**i)*math.log(u) for i in range(10))
    if s_int == float("inf"): return len(fallback(theta)[1])*t1
    raise ValueError("invalid state")

def grav_mode(s: float, theta: float, k: float, p: float, u: float) -> Tuple[str,float]:
    """Λ‑Gravitational"""
    s_int = int(s) if s != float("inf") else float("inf")
    if s_int == 1: return "Accelerare", time_wrap(k,p,u)
    if s_int == 0: return "Stagnare", CFG.t1*math.log(u)
    if s_int == -1: return "Frânare", -time_wrap(k,p,u)
    if s_int == float("inf"): return fallback(theta)[0], 0.0
    raise ValueError("invalid state")

# ======================================================
# REST API (FastAPI)
# ======================================================

app = FastAPI(title="VENOM Λ-Core API", version="1.0.0")

@app.get("/")
def root():
    return {
        "service": "VENOM Λ-Core API",
        "version": "1.0.0",
        "endpoints": {
            "REST": {
                "/time_wrap": "GET - Calculate time wrap",
                "/fractal_total": "GET - Fractal tetrastrat decision",
                "/mobius_time": "GET - Möbius temporal scaling",
                "/grav_mode": "GET - Gravitational mode"
            },
            "gRPC": f"localhost:{CFG.grpc_port}" if GRPC_AVAILABLE else "Not available"
        }
    }

@app.get("/time_wrap")
def api_time_wrap(k: float=CFG.k, p: float=CFG.p, u: float=CFG.u):
    """Calculate Λ‑TimeWrap"""
    return {"TΛ": time_wrap(k,p,u)}

@app.get("/fractal_total")
def api_fractal_total(s: float=float("inf"), theta: float=0.5):
    """Λ‑Fractal Tetrastrat decision"""
    state, ops = fractal_total(s,theta)
    return {"state": state, "ops": ops}

@app.get("/mobius_time")
def api_mobius_time(s: float=float("inf"), theta: float=0.5, k: float=CFG.k, p: float=CFG.p, u: float=CFG.u):
    """Λ‑Möbius Temporal"""
    return {"Möbius": mobius_time(s,k,p,u,theta)}

@app.get("/grav_mode")
def api_grav_mode(s: float=float("inf"), theta: float=0.5, k: float=CFG.k, p: float=CFG.p, u: float=CFG.u):
    """Λ‑Gravitational mode"""
    mode,val = grav_mode(s,theta,k,p,u)
    return {"mode": mode, "value": val}

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "venom-api"}

# ======================================================
# gRPC Server (placeholder - needs venom_pb2)
# ======================================================

# Uncomment after generating protobuf files:
# class VenomServicer(venom_pb2_grpc.VenomServicer):
#     def TimeWrap(self, request, context):
#         result = time_wrap(request.k, request.p, request.u)
#         return venom_pb2.FloatReply(value=result)
#     
#     def FractalTotal(self, request, context):
#         state, ops = fractal_total(request.s, request.theta)
#         return venom_pb2.FractalReply(state=state, ops=ops)
#     
#     def MobiusTime(self, request, context):
#         result = mobius_time(request.s, request.k, request.p, request.u, request.theta)
#         return venom_pb2.FloatReply(value=result)
#     
#     def GravMode(self, request, context):
#         mode, value = grav_mode(request.s, request.theta, request.k, request.p, request.u)
#         return venom_pb2.GravReply(mode=mode, value=value)

def serve_grpc():
    """Start gRPC server (placeholder)"""
    if not GRPC_AVAILABLE:
        print("[WARNING] gRPC not available")
        return
    
    # Uncomment after generating protobuf:
    # server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    # venom_pb2_grpc.add_VenomServicer_to_server(VenomServicer(), server)
    # server.add_insecure_port(f"127.0.0.1:{CFG.grpc_port}")
    # print(f"[gRPC] Starting on port {CFG.grpc_port}")
    # server.start()
    # server.wait_for_termination()
    pass

# ======================================================
# Entry point
# ======================================================

if __name__ == "__main__":
    # Start gRPC in background thread
    import threading
    if GRPC_AVAILABLE:
        grpc_thread = threading.Thread(target=serve_grpc, daemon=True)
        grpc_thread.start()
    
    # Start REST API
    print(f"[REST] Starting on port {CFG.rest_port}")
    uvicorn.run(app, host="127.0.0.1", port=CFG.rest_port)
