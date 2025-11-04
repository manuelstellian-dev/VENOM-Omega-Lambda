"""
Fractal Time Compression Module
Core mathematical functions for VENOM time manipulation
"""

import logging
import signal
import sys
from dataclasses import dataclass
from typing import Optional
import math

logger = logging.getLogger(__name__)


@dataclass
class Config:
    """Configuration for fractal computations"""
    k: float = 1.5  # Kernel multiplier
    p: float = 0.75  # Parallel fraction
    u: float = 0.2  # Utilization factor
    theta: float = 0.7  # System health theta


def time_wrap(k: float, p: float, u: float, t1: float) -> float:
    """
    Apply time wrapping transformation
    
    Args:
        k: Kernel multiplier
        p: Parallel fraction
        u: Utilization factor
        t1: Original time
        
    Returns:
        Wrapped time
    """
    if t1 <= 0:
        return 0.0
    
    # Time wrap formula: T_wrap = T1 / (k × (1 + ln(1 + p)) × (1 + u))
    wrapped = t1 / (k * (1 + math.log(1 + p)) * (1 + u))
    
    logger.debug(f"time_wrap: {t1} -> {wrapped}")
    return wrapped


def fractal_total(s: float, theta: float) -> float:
    """
    Calculate fractal total speedup
    
    Args:
        s: Sequential speedup
        theta: System health theta
        
    Returns:
        Total speedup factor
    """
    # Θ(θ) = 1 + ln(1 + θ)
    theta_compressed = 1 + math.log(1 + theta)
    
    total = s * theta_compressed
    logger.debug(f"fractal_total: {total} (s={s}, θ={theta})")
    return total


def mobius_time(s: float, k: float, p: float, u: float, theta: float) -> float:
    """
    Calculate Möbius compressed time
    
    Args:
        s: Sequential time
        k, p, u: Kernel, parallel, utilization parameters
        theta: System health theta
        
    Returns:
        Compressed time
    """
    speedup = fractal_total(k * p, theta)
    compressed = s / speedup
    
    logger.debug(f"mobius_time: {s} -> {compressed}")
    return compressed


def grav_mode(s: float, theta: float, k: float, p: float, u: float) -> dict:
    """
    Gravitational mode calculation
    
    Args:
        s: Sequential time
        theta, k, p, u: System parameters
        
    Returns:
        Dictionary with mode results
    """
    compressed = mobius_time(s, k, p, u, theta)
    speedup = s / compressed if compressed > 0 else 1.0
    
    return {
        "original": s,
        "compressed": compressed,
        "speedup": speedup,
        "theta": theta,
        "efficiency": (speedup / (k * p)) if (k * p) > 0 else 0.0
    }


def update_theta(theta: float, metric: float) -> float:
    """
    Update theta based on performance metric
    
    Args:
        theta: Current theta
        metric: Performance metric [0.0-1.0]
        
    Returns:
        Updated theta
    """
    # Adaptive adjustment
    adjustment = (metric - 0.5) * 0.1
    new_theta = max(0.1, min(1.0, theta + adjustment))
    
    logger.debug(f"update_theta: {theta} -> {new_theta} (metric={metric})")
    return new_theta


def signal_handler(signum, frame):
    """Handle SIGTERM and SIGINT"""
    logger.info(f"Received signal {signum}, shutting down gracefully")
    sys.exit(0)


def main():
    """Main entry point for standalone execution"""
    logging.basicConfig(level=logging.INFO)
    
    # Register signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    logger.info("=== VENOM Fractal Time Compression Demo ===")
    
    config = Config()
    
    # Demo calculations
    sequential_time = 1000.0  # 1 second
    
    wrapped = time_wrap(config.k, config.p, config.u, sequential_time)
    logger.info(f"Time Wrap: {sequential_time}ms -> {wrapped:.2f}ms")
    
    total = fractal_total(5.0, config.theta)
    logger.info(f"Fractal Total Speedup: {total:.2f}x")
    
    compressed = mobius_time(sequential_time, config.k, config.p, config.u, config.theta)
    logger.info(f"Möbius Time: {sequential_time}ms -> {compressed:.2f}ms")
    
    grav = grav_mode(sequential_time, config.theta, config.k, config.p, config.u)
    logger.info(f"Gravitational Mode: {grav}")
    
    logger.info("=== Demo Complete ===")


if __name__ == "__main__":
    main()
