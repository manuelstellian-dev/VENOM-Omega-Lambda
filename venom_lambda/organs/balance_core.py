"""
BALANCE Organ (B: 30%) - Echilibru și Stabilitate
Flow: Stabilize  Conserve  Maintain
"""

import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)

class BalanceCore:
    """
    Organ BALANCE - Echilibru și Stabilitate
    Menține homeostazia sistemului
    """
    
    def __init__(self, genome: Dict[str, Any]):
        self.genome = genome
        self.weight = genome['weights']['B']  # 0.30
        self.state = "balanced"
        self.balance_adjustments = 0
        
        logging.info(f"⚖️ BALANCE Core initialized (weight: {self.weight})")
    
    def cycle(self, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ciclu de echilibrare
        
        Args:
            health_data: System health metrics
            
        Returns:
            Dict with cycle results
        """
        theta = health_data.get('theta', 0.5)
        
        # STABILIZE: Ajustează balanța
        stability = self.stabilize(theta)
        
        # CONSERVE: Conservă energie
        conservation = self.conserve(health_data)
        
        # MAINTAIN: Menține echilibrul
        maintenance = self.maintain()
        
        self.state = f"balanced_at_{theta:.2f}"
        self.balance_adjustments += 1
        
        return {
            "organ": "BALANCE",
            "action": "balancing",
            "stability": stability,
            "conservation": conservation,
            "maintenance": maintenance,
            "theta": theta,
            "state": self.state,
            "total_adjustments": self.balance_adjustments
        }
    
    def stabilize(self, theta: float) -> str:
        """
        Stabilizează sistemul bazat pe theta
        
        Args:
            theta: System health (0-1)
            
        Returns:
            Stability mode
        """
        if theta < 0.3:
            mode = "unwrap_mode"
            logging.info(f"⚖️ [BALANCE] Stabilizing: UNWRAP (θ={theta:.2f}) - conserve energy")
        elif theta < 0.5:
            mode = "transition_mode"
            logging.info(f"⚖️ [BALANCE] Stabilizing: TRANSITION (θ={theta:.2f})")
        elif theta < 0.7:
            mode = "balance_mode"
            logging.info(f"⚖️ [BALANCE] Stabilizing: OPTIMAL (θ={theta:.2f})")
        elif theta < 0.9:
            mode = "wrap_mode"
            logging.info(f"⚖️ [BALANCE] Stabilizing: WRAP (θ={theta:.2f}) - high performance")
        else:
            mode = "optimize_mode"
            logging.info(f"⚖️ [BALANCE] Stabilizing: OPTIMIZE (θ={theta:.2f}) - maximum power")
        
        return mode
    
    def conserve(self, health_data: Dict[str, Any]) -> str:
        """
        Conservă energie când e necesar
        
        Args:
            health_data: System health metrics
            
        Returns:
            Conservation level
        """
        battery_level = health_data.get('battery_level', 100)
        
        if battery_level < 20:
            conservation = "aggressive_conservation"
            logging.warning(f"🔋 [BALANCE] Conservation: AGGRESSIVE (battery: {battery_level}%)")
        elif battery_level < 50:
            conservation = "moderate_conservation"
            logging.info(f"🔋 [BALANCE] Conservation: MODERATE (battery: {battery_level}%)")
        else:
            conservation = "normal_operation"
            logging.debug(f"🔋 [BALANCE] Conservation: NORMAL (battery: {battery_level}%)")
        
        return conservation
    
    def maintain(self) -> str:
        """
        Menține echilibrul (homeostasis)
        
        Returns:
            Maintenance status
        """
        # Continuous homeostasis maintenance
        return "homeostasis_active"
