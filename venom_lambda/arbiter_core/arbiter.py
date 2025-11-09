"""
Lambda Arbiter - Nucleu Decizional
Coordonează cele 4 organe [R, B, E, O] folosind ADN fractal
"""

import json
import logging
import sys
from pathlib import Path
from typing import Dict, Any, Tuple, List
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class LambdaArbiter:
    """
    Arbiter Λ - Nucleu Decizional
    Coordonează cele 4 organe [R, B, E, O] folosind genome weights
    """
    
    def __init__(self, genome_path: str = None):
        """
        Initialize Lambda Arbiter with genome
        
        Args:
            genome_path: Path to genome.json file
        """
        # Default genome path
        if genome_path is None:
            genome_path = Path(__file__).parent / "genome.json"
        
        # Load genome
        try:
            with open(genome_path, 'r') as f:
                genome_data = json.load(f)
                self.genome = genome_data['Λ-genome']
        except Exception as e:
            logging.error(f"Failed to load genome: {e}")
            # Fallback to default genome
            self.genome = {
                "bases": ["R", "B", "E", "O"],
                "weights": {
                    "R": 0.20,
                    "B": 0.30,
                    "E": 0.15,
                    "O": 0.30,
                    "Λ": 0.05
                },
                "pulses": "fractal_parallel"
            }
        
        # Initialize organs (lazy import to avoid circular dependencies)
        self.organs = {}
        self._init_organs()
        
        logging.info(f"🧬 Lambda Arbiter initialized with genome: {self.genome['weights']}")
    
    def _init_organs(self):
        """Initialize all 4 organs"""
        try:
            # Import organs
            sys.path.insert(0, str(Path(__file__).parent.parent))
            
            from organs.regen_core import RegenCore
            from organs.balance_core import BalanceCore
            from organs.entropy_core import EntropyCore
            from organs.optimize_core import OptimizeCore
            
            # Create organ instances
            self.organs = {
                "REGEN": RegenCore(self.genome),
                "BALANCE": BalanceCore(self.genome),
                "ENTROPY": EntropyCore(self.genome),
                "OPTIMIZE": OptimizeCore(self.genome)
            }
            
            logging.info(f"✅ Initialized {len(self.organs)} organs")
            
        except Exception as e:
            logging.error(f"Failed to initialize organs: {e}")
            self.organs = {}
    
    def time_wrap(self, health_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Time Wrap: Execuție paralelă a tuturor organelor
        Toate lucrează simultan → rezultate integrate
        
        Args:
            health_data: System health metrics (theta, cpu, memory, thermal, etc.)
        
        Returns:
            Dict with integrated results from all organs
        """
        if health_data is None:
            health_data = self.get_default_health()
        
        results = {}
        
        # Parallel execution of all organs
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Submit all organ cycles
            futures = {
                executor.submit(organ.cycle, health_data): name
                for name, organ in self.organs.items()
            }
            
            # Collect results as they complete
            for future in as_completed(futures):
                organ_name = futures[future]
                try:
                    result = future.result(timeout=5.0)
                    results[organ_name] = result
                    logging.debug(f"[{organ_name}] Cycle completed: {result.get('action', 'unknown')}")
                except Exception as e:
                    logging.error(f"[{organ_name}] Error: {e}")
                    results[organ_name] = {"error": str(e)}
        
        # Recalibrate based on genome weights
        integrated = self.recalibrate(results)
        
        return integrated
    
    def recalibrate(self, organ_results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Integrează rezultatele organelor bazat pe ADN weights
        
        Args:
            organ_results: Results from each organ
        
        Returns:
            Integrated results with weighted score
        """
        weights = self.genome['weights']
        
        # Calculate weighted integration score
        integrated_score = 0.0
        total_weight = 0.0
        
        for organ_name, result in organ_results.items():
            # Get organ weight (R, B, E, O)
            organ_key = organ_name[0]  # First letter: R, B, E, O
            weight = weights.get(organ_key, 0.25)
            
            # Simple scoring based on action success
            if 'action' in result and result['action'] != 'error':
                organ_score = 1.0
            else:
                organ_score = 0.0
            
            integrated_score += weight * organ_score
            total_weight += weight
        
        # Normalize score
        if total_weight > 0:
            integrated_score /= total_weight
        
        return {
            "organs": organ_results,
            "integrated_score": integrated_score,
            "genome_balance": weights,
            "timestamp": self._get_timestamp()
        }
    
    def get_default_health(self) -> Dict[str, Any]:
        """
        Default health data for testing
        
        Returns:
            Dict with default system health metrics
        """
        return {
            "theta": 0.7,
            "cpu_health": 0.8,
            "memory_health": 0.85,
            "thermal_health": 0.9,
            "battery_level": 80,
            "model_corruption": False,
            "cache_size": 50_000_000,
            "cpu_cores": 8
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

def main():
    """Test the Lambda Arbiter"""
    logging.info("🧬 Lambda Arbiter Test")
    
    # Create arbiter
    arbiter = LambdaArbiter()
    
    # Test health data
    health_data = {
        "theta": 0.85,
        "cpu_health": 0.9,
        "memory_health": 0.8,
        "thermal_health": 0.95,
        "battery_level": 90
    }
    
    # Execute time_wrap
    result = arbiter.time_wrap(health_data)
    
    # Print results
    logging.info(f"📊 Time Wrap Results:")
    logging.info(f"   Integrated Score: {result['integrated_score']:.3f}")
    logging.info(f"   Genome Balance: {result['genome_balance']}")
    
    for organ_name, organ_result in result['organs'].items():
        logging.info(f"   [{organ_name}]: {organ_result}")

if __name__ == "__main__":
    main()
