"""
Lambda Arbiter - Central coordinator for Λ-Genesis layer
Implements time-wrapping and recalibration based on organ feedback
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)


class LambdaArbiter:
    """
    Lambda Arbiter coordinates the Λ-Genesis organism
    - Time wrapping based on hardware health
    - Recalibration from organ results
    - Genome-based parameter management
    """
    
    def __init__(self, genome_path: str = None):
        """
        Initialize Lambda Arbiter
        
        Args:
            genome_path: Path to genome.json configuration
        """
        self.genome_path = genome_path or self._default_genome_path()
        self.genome = self._load_genome()
        self.health_data = self.get_default_health()
        
        logger.info(f"LambdaArbiter initialized with genome: {self.genome_path}")
    
    def _default_genome_path(self) -> str:
        """Get default genome.json path"""
        return str(Path(__file__).parent / "genome.json")
    
    def _load_genome(self) -> Dict[str, Any]:
        """Load Λ-genome configuration"""
        try:
            with open(self.genome_path, 'r') as f:
                genome = json.load(f)
            logger.info(f"Loaded genome: {genome.get('Λ-genome', {}).get('bases', [])}")
            return genome
        except FileNotFoundError:
            logger.warning(f"Genome file not found: {self.genome_path}, using defaults")
            return self._default_genome()
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse genome: {e}")
            return self._default_genome()
    
    def _default_genome(self) -> Dict[str, Any]:
        """Return default genome configuration"""
        return {
            "Λ-genome": {
                "bases": ["R", "B", "E", "O"],
                "weights": {
                    "R": 0.20,  # Regenerate
                    "B": 0.30,  # Balance
                    "E": 0.15,  # Entropy
                    "O": 0.30,  # Optimize
                    "Λ": 0.05   # Lambda core
                },
                "pulses": "fractal_parallel"
            }
        }
    
    def time_wrap(self, health_data: Dict[str, float]) -> Dict[str, Any]:
        """
        Apply time-wrapping transformation based on health metrics
        
        Args:
            health_data: Dictionary with health metrics (theta, cpu, memory, thermal)
            
        Returns:
            Time-wrapped result with integrated Lambda score
        """
        logger.debug(f"Time wrapping with health: {health_data}")
        
        self.health_data = health_data
        
        # Extract health metrics
        theta = health_data.get('theta', 0.7)
        cpu = health_data.get('cpu', 0.8)
        memory = health_data.get('memory', 0.8)
        thermal = health_data.get('thermal', 0.8)
        
        # Calculate Lambda score based on genome weights
        weights = self.genome.get("Λ-genome", {}).get("weights", {})
        
        # Weighted health aggregation
        lambda_score = (
            weights.get("R", 0.2) * theta +
            weights.get("B", 0.3) * cpu +
            weights.get("E", 0.15) * memory +
            weights.get("O", 0.3) * thermal +
            weights.get("Λ", 0.05) * 1.0  # Base Lambda factor
        )
        
        # Scale to [10, 832]
        lambda_score = 10 + lambda_score * 822
        
        result = {
            "lambda_score": lambda_score,
            "theta": theta,
            "health": {
                "cpu": cpu,
                "memory": memory,
                "thermal": thermal
            },
            "timestamp": self._get_timestamp()
        }
        
        logger.info(f"Time wrap complete: Λ={lambda_score:.2f}")
        return result
    
    def recalibrate(self, organ_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recalibrate parameters based on organ execution results
        
        Args:
            organ_results: Results from R, B, E, O organs
            
        Returns:
            Recalibration adjustments
        """
        logger.debug(f"Recalibrating from organs: {organ_results.keys()}")
        
        adjustments = {
            "weights_updated": False,
            "performance_delta": 0.0
        }
        
        # TODO: Implement adaptive weight adjustment based on organ performance
        
        logger.info("Recalibration complete")
        return adjustments
    
    def get_default_health(self) -> Dict[str, float]:
        """Get default health data"""
        return {
            "theta": 0.7,
            "cpu": 0.8,
            "memory": 0.8,
            "thermal": 0.8
        }
    
    def _get_timestamp(self) -> int:
        """Get current timestamp in milliseconds"""
        import time
        return int(time.time() * 1000)
    
    def get_genome_info(self) -> Dict[str, Any]:
        """Get genome configuration info"""
        return self.genome.get("Λ-genome", {})
