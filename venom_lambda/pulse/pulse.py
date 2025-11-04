"""
Pulse Fractal - The heartbeat of the Λ-Genesis organism
Operates on ~1ms fractal beat intervals
"""

import logging
import asyncio
import time
from typing import Optional, Callable

logger = logging.getLogger(__name__)


class PulseFractal:
    """
    Fractal Pulse Generator
    Coordinates organism-wide timing and synchronization
    """
    
    def __init__(self, lambda_arbiter, mobius_engine=None):
        """
        Initialize Pulse Fractal
        
        Args:
            lambda_arbiter: Reference to LambdaArbiter
            mobius_engine: Optional reference to MobiusEngine for time compression
        """
        self.lambda_arbiter = lambda_arbiter
        self.mobius_engine = mobius_engine
        self.is_beating = False
        self.beat_count = 0
        self.beat_interval_ms = 1.0  # 1ms default
        self.pulse_task: Optional[asyncio.Task] = None
        
        logger.info(f"PulseFractal initialized (interval={self.beat_interval_ms}ms)")
    
    async def beat(self):
        """Single pulse beat"""
        self.beat_count += 1
        timestamp = int(time.time() * 1000)
        
        # Log every 1000 beats (1 second)
        if self.beat_count % 1000 == 0:
            self.log_pulse()
        
        return {
            "beat": self.beat_count,
            "timestamp": timestamp,
            "interval_ms": self.beat_interval_ms
        }
    
    def log_pulse(self):
        """Log pulse status"""
        logger.debug(f"Pulse: {self.beat_count} beats ({self.beat_count / 1000:.1f}s)")
    
    async def start(self):
        """Start the fractal pulse"""
        if self.is_beating:
            logger.warning("Pulse already started")
            return
        
        self.is_beating = True
        logger.info("Pulse started")
        
        self.pulse_task = asyncio.create_task(self._pulse_loop())
    
    async def _pulse_loop(self):
        """Main pulse loop"""
        while self.is_beating:
            try:
                await self.beat()
                await asyncio.sleep(self.beat_interval_ms / 1000.0)
            except Exception as e:
                logger.error(f"Pulse error: {e}")
                await asyncio.sleep(0.01)
    
    async def stop(self):
        """Stop the fractal pulse"""
        self.is_beating = False
        if self.pulse_task:
            self.pulse_task.cancel()
            try:
                await self.pulse_task
            except asyncio.CancelledError:
                pass
        
        logger.info(f"Pulse stopped after {self.beat_count} beats")
    
    def get_status(self):
        """Get pulse status"""
        return {
            "beating": self.is_beating,
            "beat_count": self.beat_count,
            "interval_ms": self.beat_interval_ms,
            "uptime_s": self.beat_count * self.beat_interval_ms / 1000.0
        }
