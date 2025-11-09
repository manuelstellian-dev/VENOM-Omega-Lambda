"""
Pulse Fractal - Inima Digitală
Beat: 1ms fractal → Time Wrap parallel execution
Synchronized with Möbius Engine (Ω)
"""

import threading
import time
import logging
from pathlib import Path
from typing import Optional, Dict, Any

logging.basicConfig(level=logging.INFO)

class PulseFractal:
    """
    Inima Fractală - Time Wrap Biologic
    Beat: 1ms → toate organele [R,B,E,O] lucrează simultan
    """
    
    def __init__(self, lambda_arbiter, mobius_engine=None):
        """
        Initialize Pulse Fractal
        
        Args:
            lambda_arbiter: LambdaArbiter instance
            mobius_engine: Optional Möbius Engine for temporal compression
        """
        self.lambda_arbiter = lambda_arbiter
        self.mobius_engine = mobius_engine
        self.alive = False
        self.beat_count = 0
        self.total_beats = 0
        
        # Cycle time from Möbius Engine or default 1ms
        if mobius_engine:
            self.cycle_time = 0.001  # Synchronized with Möbius
            self.adaptive_timing = True
        else:
            self.cycle_time = 0.001  # 1ms fractal beat
            self.adaptive_timing = False
        
        # Pulse log
        self.log_path = Path.home() / ".venom" / "pulse.log"
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Performance metrics
        self.avg_beat_time = 0.0
        self.min_beat_time = float('inf')
        self.max_beat_time = 0.0
        
        logging.info(f"💓 Pulse Fractal initialized (cycle: {self.cycle_time * 1000:.3f}ms)")
    
    def beat(self):
        """
        Puls fractal: Time Wrap
        Toate organele [R,B,E,O] lucrează simultan
        """
        logging.info(f"💓 Pulse Fractal: BEATING...")
        
        while self.alive:
            beat_start = time.time()
            
            try:
                # TIME WRAP: Execuție paralelă organe
                results = self.lambda_arbiter.time_wrap()
                
                # Log pulse
                self.log_pulse(results)
                
                # Increment beat counter
                self.beat_count += 1
                self.total_beats += 1
                
                # Calculate beat duration
                beat_duration = time.time() - beat_start
                self._update_metrics(beat_duration)
                
                # Adjust cycle time from Möbius if available
                if self.adaptive_timing and self.mobius_engine:
                    adjusted_cycle = self._calculate_adaptive_cycle()
                    sleep_time = max(0, adjusted_cycle - beat_duration)
                else:
                    sleep_time = max(0, self.cycle_time - beat_duration)
                
                # Sleep until next beat
                if sleep_time > 0:
                    time.sleep(sleep_time)
                
                # Log milestone beats
                if self.beat_count % 1000 == 0:
                    self._log_milestone()
                
            except Exception as e:
                logging.error(f"💓 Pulse error: {e}")
                time.sleep(self.cycle_time)
    
    def log_pulse(self, results: Dict[str, Any]):
        """
        Log puls vital
        
        Args:
            results: Results from Lambda time_wrap
        """
        try:
            timestamp = time.time()
            
            # Append to log file
            with open(self.log_path, "a") as f:
                log_entry = f"[PULSE {self.beat_count}] {timestamp}: {results}\n"
                f.write(log_entry)
            
            # Debug log every 100 beats
            if self.beat_count % 100 == 0:
                score = results.get('integrated_score', 0)
                logging.debug(f"💓 Pulse {self.beat_count}: Score={score:.3f}")
                
        except Exception as e:
            logging.error(f"Log pulse error: {e}")
    
    def start(self):
        """
        Pornește inima fractală
        """
        if self.alive:
            logging.warning(f"💓 Pulse already running")
            return
        
        self.alive = True
        self.beat_count = 0
        
        # Start beat thread
        beat_thread = threading.Thread(target=self.beat, daemon=True)
        beat_thread.start()
        
        logging.info(f"💓 Pulse Fractal: STARTED (thread: {beat_thread.name})")
    
    def stop(self):
        """
        Oprește inima fractală
        """
        if not self.alive:
            logging.warning(f"💓 Pulse not running")
            return
        
        self.alive = False
        
        # Log final statistics
        self._log_final_stats()
        
        logging.info(f"💓 Pulse Fractal: STOPPED (total beats: {self.total_beats})")
    
    def _calculate_adaptive_cycle(self) -> float:
        """
        Calculate adaptive cycle time based on Möbius compression
        
        Returns:
            Adjusted cycle time in seconds
        """
        try:
            # Get compression factor from Möbius
            # compression = self.mobius_engine.total_speedup()
            # For now, use fixed compression
            compression = 1.0
            
            # Adaptive cycle time based on compression
            adjusted_cycle = self.cycle_time / (compression ** 0.1)
            
            # Clamp to reasonable range [0.5ms, 10ms]
            return max(0.0005, min(adjusted_cycle, 0.01))
            
        except Exception as e:
            logging.error(f"Adaptive cycle calculation error: {e}")
            return self.cycle_time
    
    def _update_metrics(self, beat_duration: float):
        """
        Update performance metrics
        
        Args:
            beat_duration: Duration of this beat in seconds
        """
        # Update average (exponential moving average)
        alpha = 0.1
        self.avg_beat_time = alpha * beat_duration + (1 - alpha) * self.avg_beat_time
        
        # Update min/max
        self.min_beat_time = min(self.min_beat_time, beat_duration)
        self.max_beat_time = max(self.max_beat_time, beat_duration)
    
    def _log_milestone(self):
        """
        Log milestone statistics (every 1000 beats)
        """
        logging.info(f"""
💓 Pulse Milestone: {self.beat_count} beats
   - Avg beat time: {self.avg_beat_time * 1000:.3f}ms
   - Min beat time: {self.min_beat_time * 1000:.3f}ms
   - Max beat time: {self.max_beat_time * 1000:.3f}ms
   - Total beats: {self.total_beats}
        """.strip())
    
    def _log_final_stats(self):
        """
        Log final statistics when stopping
        """
        uptime = self.total_beats * self.cycle_time
        
        logging.info(f"""
💓 Pulse Final Statistics:
   - Total beats: {self.total_beats}
   - Uptime: {uptime:.2f}s ({uptime / 60:.2f}min)
   - Avg beat time: {self.avg_beat_time * 1000:.3f}ms
   - Min beat time: {self.min_beat_time * 1000:.3f}ms
   - Max beat time: {self.max_beat_time * 1000:.3f}ms
   - Cycle time: {self.cycle_time * 1000:.3f}ms
        """.strip())
    
    def get_vitals(self) -> Dict[str, Any]:
        """
        Get pulse vitals
        
        Returns:
            Dict with pulse statistics
        """
        return {
            "alive": self.alive,
            "beat_count": self.beat_count,
            "total_beats": self.total_beats,
            "cycle_time_ms": self.cycle_time * 1000,
            "avg_beat_time_ms": self.avg_beat_time * 1000,
            "min_beat_time_ms": self.min_beat_time * 1000,
            "max_beat_time_ms": self.max_beat_time * 1000,
            "adaptive_timing": self.adaptive_timing
        }


def main():
    """
    Test Pulse Fractal
    """
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    from arbiter_core.arbiter import LambdaArbiter
    
    logging.info("💓 Testing Pulse Fractal...")
    
    # Create arbiter
    arbiter = LambdaArbiter()
    
    # Create pulse
    pulse = PulseFractal(arbiter)
    
    # Start pulse
    pulse.start()
    
    # Run for 5 seconds
    time.sleep(5)
    
    # Get vitals
    vitals = pulse.get_vitals()
    logging.info(f"💓 Pulse vitals: {vitals}")
    
    # Stop pulse
    pulse.stop()
    
    logging.info("💓 Test completed")


if __name__ == "__main__":
    main()
