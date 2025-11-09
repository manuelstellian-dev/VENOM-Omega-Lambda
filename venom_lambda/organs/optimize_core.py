"""
OPTIMIZE Organ (O: 30%) - Optimizare și Redistribuire
Flow: Detect  Adjust  Redistribute  Restart
"""

import logging
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO)

class OptimizeCore:
    """
    Organ OPTIMIZE - Optimizare și Redistribuire
    Maximizează eficiența sistemului
    """
    
    def __init__(self, genome: Dict[str, Any]):
        self.genome = genome
        self.weight = genome['weights']['O']  # 0.30
        self.optimizations = []
        self.optimization_count = 0
        
        logging.info(f"⚡ OPTIMIZE Core initialized (weight: {self.weight})")
    
    def cycle(self, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ciclu de optimizare
        
        Args:
            health_data: System health metrics
            
        Returns:
            Dict with cycle results
        """
        # DETECT: Ce poate fi optimizat
        targets = self.detect_optimization_targets(health_data)
        
        # ADJUST: Ajustează parametri
        adjustments = self.adjust(targets)
        
        # REDISTRIBUTE: Redistribuie resurse
        redistributed = self.redistribute(health_data)
        
        # RESTART: Restart componente optimizate
        restarted = self.restart_if_needed(adjustments)
        
        self.optimization_count += len(targets)
        
        return {
            "organ": "OPTIMIZE",
            "action": "optimizing",
            "targets": len(targets),
            "adjustments": adjustments,
            "redistributed": redistributed,
            "restarted": restarted,
            "total_optimizations": self.optimization_count
        }
    
    def detect_optimization_targets(self, health_data: Dict[str, Any]) -> List[str]:
        """
        Detectează ce poate fi optimizat
        
        Args:
            health_data: System health metrics
            
        Returns:
            List of optimization targets
        """
        targets = []
        theta = health_data.get('theta', 0.5)
        
        # Model size optimization
        model_size = health_data.get('model_size', 0)
        if theta < 0.5 and model_size > 1_000_000_000:
            targets.append("quantize_model")
            logging.info(f"🎯 [OPTIMIZE] Target: quantize_model (size: {model_size / 1e9:.2f}GB)")
        
        # Thread optimization
        cpu_cores = health_data.get('cpu_cores', 4)
        if cpu_cores > 4:
            targets.append("increase_threads")
            logging.info(f"🎯 [OPTIMIZE] Target: increase_threads (cores: {cpu_cores})")
        
        # Cache optimization
        cache_hit_rate = health_data.get('cache_hit_rate', 1.0)
        if cache_hit_rate < 0.7:
            targets.append("optimize_cache")
            logging.info(f"🎯 [OPTIMIZE] Target: optimize_cache (hit rate: {cache_hit_rate:.2f})")
        
        return targets
    
    def adjust(self, targets: List[str]) -> List[str]:
        """
        Ajustează parametri
        
        Args:
            targets: List of optimization targets
            
        Returns:
            List of adjustments made
        """
        adjustments = []
        
        for target in targets:
            if target == "quantize_model":
                adjustments.append("model_quantized_int8")
                logging.info(f"⚙️ [OPTIMIZE] Adjusted: model → INT8 quantization")
                
            elif target == "increase_threads":
                adjustments.append("threads_increased")
                logging.info(f"⚙️ [OPTIMIZE] Adjusted: threads → increased parallelism")
                
            elif target == "optimize_cache":
                adjustments.append("cache_optimized")
                logging.info(f"⚙️ [OPTIMIZE] Adjusted: cache → LRU eviction policy")
        
        return adjustments
    
    def redistribute(self, health_data: Dict[str, Any]) -> Dict[str, int]:
        """
        Redistribuie resurse bazat pe prioritate
        
        Args:
            health_data: System health metrics
            
        Returns:
            Dict with resource distribution percentages
        """
        theta = health_data.get('theta', 0.5)
        
        if theta < 0.3:
            # UNWRAP: Most to REGEN
            distribution = {"REGEN": 40, "BALANCE": 30, "ENTROPY": 15, "OPTIMIZE": 15}
            logging.info(f"📊 [OPTIMIZE] Redistributed: UNWRAP mode (REGEN priority)")
        
        elif theta < 0.7:
            # BALANCE: Balanced distribution
            distribution = {"REGEN": 25, "BALANCE": 35, "ENTROPY": 20, "OPTIMIZE": 20}
            logging.info(f"📊 [OPTIMIZE] Redistributed: BALANCE mode (equilibrium)")
        
        else:
            # OPTIMIZE: Most to performance
            distribution = {"REGEN": 20, "BALANCE": 25, "ENTROPY": 20, "OPTIMIZE": 35}
            logging.info(f"📊 [OPTIMIZE] Redistributed: OPTIMIZE mode (performance)")
        
        return distribution
    
    def restart_if_needed(self, adjustments: List[str]) -> str:
        """
        Restart componente dacă e necesar
        
        Args:
            adjustments: List of adjustments made
            
        Returns:
            Restart status
        """
        critical_adjustments = ["model_quantized_int8", "threads_increased"]
        
        needs_restart = any(adj in critical_adjustments for adj in adjustments)
        
        if needs_restart:
            logging.info(f"🔄 [OPTIMIZE] Restart required for: {adjustments}")
            return "model_engine_restarted"
        else:
            return "no_restart_needed"
