#!/usr/bin/env python3
# lambda/core/fractal.py

"""
fractal.py – VENOM Λ‑Core fractal worker

Implements: Λ‑TimeWrap, Λ‑Fractal Tetrastrat, Λ‑Möbius Temporal, Λ‑Gravitational
"""

import math
import os
import time
import json
import logging
import signal
from pathlib import Path
from dataclasses import dataclass
from typing import Tuple, List

# -------------------------------------------------------------------
# Immutable configuration
# -------------------------------------------------------------------

@dataclass(frozen=True)
class Config:
    theta_low: float = 0.3          # minimum resilience
    theta_high: float = 0.7         # high resilience
    t1: float = 1.0                 # base time unit
    k: float = 100.0                # scaling factor
    p: float = 10.0                 # pressure factor
    u: float = 1e6                  # utility / workload magnitude
    mobius_iter: int = 10           # series depth for Möbius temporal
    log_path: Path = Path.home() / "venom" / "run" / "fractal.log"

CFG = Config()

# -------------------------------------------------------------------
# Logging (thread‑safe, atomic append)
# -------------------------------------------------------------------

CFG.log_path.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=CFG.log_path,
    level=logging.INFO,
    format="[+] %(asctime)s %(message)s",
    datefmt="%c",
)

def log(msg: str) -> None:
    """Append a message to the fractal log."""
    logging.info(msg)
    print(f"[FRACTAL] {msg}")  # Also print to console

# -------------------------------------------------------------------
# Mathematical primitives
# -------------------------------------------------------------------

def time_wrap(k: float, p: float, u: float, t1: float = CFG.t1) -> float:
    """
    Λ‑TimeWrap – finite execution time
    
    Formula: T_Λ = (T1 * ln(U)) / (1 - 1/(kP))
    
    Args:
        k: Scaling factor
        p: Pressure factor
        u: Utility/workload magnitude
        t1: Base time unit
        
    Returns:
        Compressed time value
    """
    if k * p == 1:
        raise ValueError("k * p must not equal 1 (division by zero)")
    
    result = (t1 * math.log(u)) / (1 - 1 / (k * p))
    return result

# State map for fractal tetrastrat
_STATE_MAP: dict[int, Tuple[str, List[str]]] = {
    1: ("Regen",   ["Scan", "Detect", "Quarantine", "Heal", "Improve", "Reinvest"]),
    0: ("Neutral", ["Scan", "Detect", "Quarantine", "Heal", "Neutralize", "Stabilize"]),
    -1: ("Entropy", ["Reinvest_neg", "Degrade", "Infect", "Spread", "Ignore", "Blind"]),
}

def fallback(theta: float) -> Tuple[str, List[str]]:
    """
    Λ‑Fallback meta‑layer (state ∞)
    
    Args:
        theta: System resilience (0-1)
        
    Returns:
        Tuple of (state_name, operations)
    """
    if theta >= CFG.theta_high:
        return "Fallback→+1", ["Regen"]
    if theta >= CFG.theta_low:
        return "Fallback→0", ["Neutral"]
    return "Fallback→-1", ["Entropy"]

def fractal_total(s: int, theta: float) -> Tuple[str, List[str]]:
    """
    Λ‑Fractal Tetrastrat decision
    
    Args:
        s: State (1, 0, -1, or inf)
        theta: System resilience
        
    Returns:
        Tuple of (state_name, operations)
    """
    if s in _STATE_MAP:
        return _STATE_MAP[s]
    if s == float("inf"):
        return fallback(theta)
    raise ValueError(f"Invalid state {s}")

def mobius_time(s: int, k: float, p: float, u: float,
                theta: float, t1: float = CFG.t1) -> float:
    """
    Λ‑Möbius Temporal – time scaling per state
    
    Args:
        s: State (1, 0, -1, or inf)
        k: Scaling factor
        p: Pressure factor
        u: Utility magnitude
        theta: System resilience
        t1: Base time unit
        
    Returns:
        Temporal scaling value
    """
    if s == 1:
        return time_wrap(k, p, u, t1)
    if s == 0:
        return t1 * math.log(u)
    if s == -1:
        # Approximate divergent series
        return sum(t1 * ((k * p) ** i) * math.log(u) for i in range(CFG.mobius_iter))
    if s == float("inf"):
        _, ops = fallback(theta)
        return len(ops) * t1
    raise ValueError(f"Unsupported state {s}")

def grav_mode(s: int, theta: float, k: float, p: float, u: float) -> Tuple[str, float]:
    """
    Λ‑Gravitational mode (accelerate / stagnate / brake)
    
    Args:
        s: State
        theta: System resilience
        k: Scaling factor
        p: Pressure factor
        u: Utility magnitude
        
    Returns:
        Tuple of (mode_name, value)
    """
    if s == 1:
        return "Accelerare", time_wrap(k, p, u)
    if s == 0:
        return "Stagnare", CFG.t1 * math.log(u)
    if s == -1:
        return "Frânare", -time_wrap(k, p, u)
    if s == float("inf"):
        mode, _ = fallback(theta)
        return mode, 0.0
    raise ValueError(f"Invalid state {s}")

# -------------------------------------------------------------------
# Adaptive resilience (θ) update
# -------------------------------------------------------------------

def update_theta(theta: float, metric: float) -> float:
    """
    Smoothly move theta toward a normalized system metric (0‑1).
    Positive metric raises resilience; low metric lowers it.
    
    Args:
        theta: Current theta value
        metric: Normalized system metric (0-1)
        
    Returns:
        Updated theta value
    """
    delta = 0.05 * (metric - theta)   # smoothing factor
    return min(max(theta + delta, 0.0), 1.0)

# -------------------------------------------------------------------
# Signal handling for graceful shutdown
# -------------------------------------------------------------------

_stop_requested = False

def _handle_sigterm(signum, frame):
    global _stop_requested
    _stop_requested = True
    log("SIGTERM received – shutting down gracefully")

signal.signal(signal.SIGINT, _handle_sigterm)
signal.signal(signal.SIGTERM, _handle_sigterm)

# -------------------------------------------------------------------
# Main worker loop
# -------------------------------------------------------------------

def main() -> None:
    """Entry point for the Λ‑Fractal worker."""
    theta = 0.5  # initial resilience; can be derived from health checks
    log("Λ‑Fractal worker started")
    
    cycle_count = 0
    
    while not _stop_requested:
        cycle_count += 1
        
        # ----------------------------------------------------------
        # Decision based on the "infinite" fallback state
        # ----------------------------------------------------------
        state, ops = fractal_total(float("inf"), theta)
        t_effective = time_wrap(CFG.k, CFG.p, CFG.u)
        
        log(f"Cycle {cycle_count}: Θ={theta:.2f} | State={state} | Ops={ops} | TΛ={t_effective:.4f}")
        
        # ----------------------------------------------------------
        # Simulated execution of each operation
        # ----------------------------------------------------------
        for op in ops:
            log(f" → Executing {op}")
        
        # ----------------------------------------------------------
        # Example metric: normalized 1‑minute load average
        # ----------------------------------------------------------
        try:
            load_norm = min(max(os.getloadavg()[0] / os.cpu_count(), 0.0), 1.0)
        except:
            load_norm = 0.5  # Fallback if getloadavg not available
        
        theta = update_theta(theta, load_norm)
        
        # Sleep a real second – represents compressed logical time
        time.sleep(1)
    
    log(f"Λ‑Fractal worker stopped after {cycle_count} cycles")

if __name__ == "__main__":
    main()