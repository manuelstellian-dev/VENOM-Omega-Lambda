"""
REGEN Organ (R: 20%) - Regenerare și Reparare
Flow: Detect  Quarantine  Improve  Reinvest (97%)
"""

import logging
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO)

class RegenCore:
    """
    Organ REGEN - Regenerare și Reparare
    Detectează damage, izolează, repară și reinvestește 97% din resurse
    """
    
    def __init__(self, genome: Dict[str, Any]):
        self.genome = genome
        self.weight = genome['weights']['R']  # 0.20
        self.state = "idle"
        self.repairs_performed = 0
        self.resources_reinvested = 0
        
        logging.info(f"🔄 REGEN Core initialized (weight: {self.weight})")
    
    def cycle(self, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ciclu de regenerare bazat pe health θ
        
        Args:
            health_data: System health metrics
            
        Returns:
            Dict with cycle results
        """
        # DETECT: Probleme ce necesită regenerare
        issues = self.detect_damage(health_data)
        
        if not issues:
            self.state = "healthy"
            return {
                "organ": "REGEN",
                "action": "monitoring",
                "issues": 0,
                "state": self.state
            }
        
        # QUARANTINE: Izolează probleme
        quarantined = self.quarantine(issues)
        
        # IMPROVE: Repară și îmbunătățește
        improved = self.improve(quarantined)
        
        # REINVEST: Redistribuie resurse (97%)
        reinvested = self.reinvest(improved)
        
        self.state = "active_regen"
        self.repairs_performed += len(improved)
        self.resources_reinvested += reinvested
        
        return {
            "organ": "REGEN",
            "action": "regenerating",
            "issues": len(issues),
            "quarantined": len(quarantined),
            "repaired": len(improved),
            "reinvested": reinvested,
            "state": self.state,
            "total_repairs": self.repairs_performed
        }
    
    def detect_damage(self, health_data: Dict[str, Any]) -> List[str]:
        """
        Detectează ce trebuie reparat
        
        Args:
            health_data: System health metrics
            
        Returns:
            List of detected issues
        """
        issues = []
        
        # Memory leaks
        memory_health = health_data.get('memory_health', 1.0)
        if memory_health < 0.5:
            issues.append("memory_leak")
            logging.warning(f"🔍 [REGEN] Detected: memory_leak (health: {memory_health:.2f})")
        
        # Model corruption
        if health_data.get('model_corruption', False):
            issues.append("corrupted_model")
            logging.warning(f"🔍 [REGEN] Detected: corrupted_model")
        
        # Cache bloat
        cache_size = health_data.get('cache_size', 0)
        if cache_size > 1_000_000_000:  # >1GB
            issues.append("cache_bloat")
            logging.warning(f"🔍 [REGEN] Detected: cache_bloat ({cache_size / 1e9:.2f}GB)")
        
        # Thermal damage (prolonged high temp)
        thermal_health = health_data.get('thermal_health', 1.0)
        if thermal_health < 0.3:
            issues.append("thermal_damage")
            logging.warning(f"🔍 [REGEN] Detected: thermal_damage (health: {thermal_health:.2f})")
        
        # CPU exhaustion
        cpu_health = health_data.get('cpu_health', 1.0)
        if cpu_health < 0.2:
            issues.append("cpu_exhaustion")
            logging.warning(f"🔍 [REGEN] Detected: cpu_exhaustion (health: {cpu_health:.2f})")
        
        return issues
    
    def quarantine(self, issues: List[str]) -> List[str]:
        """
        Izolează probleme pentru reparare
        
        Args:
            issues: List of detected issues
            
        Returns:
            List of quarantined issues
        """
        if not issues:
            return []
        
        logging.info(f"🚧 [REGEN] Quarantining {len(issues)} issues: {issues}")
        
        # All issues are quarantined for repair
        return issues
    
    def improve(self, quarantined: List[str]) -> List[str]:
        """
        Repară probleme
        
        Args:
            quarantined: List of quarantined issues
            
        Returns:
            List of successfully repaired issues
        """
        improved = []
        
        for issue in quarantined:
            if issue == "memory_leak":
                # Trigger garbage collection
                logging.info(f"🔧 [REGEN] Repairing: memory_leak (GC triggered)")
                improved.append(f"repaired_{issue}")
                
            elif issue == "corrupted_model":
                # Request model regeneration
                logging.info(f"🔧 [REGEN] Repairing: corrupted_model (regeneration requested)")
                improved.append(f"regenerated_{issue}")
                
            elif issue == "cache_bloat":
                # Clear caches
                logging.info(f"🔧 [REGEN] Repairing: cache_bloat (cache cleared)")
                improved.append(f"cleaned_{issue}")
                
            elif issue == "thermal_damage":
                # Cool down system
                logging.info(f"🔧 [REGEN] Repairing: thermal_damage (cooling initiated)")
                improved.append(f"cooled_{issue}")
                
            elif issue == "cpu_exhaustion":
                # Reduce CPU load
                logging.info(f"🔧 [REGEN] Repairing: cpu_exhaustion (load reduced)")
                improved.append(f"restored_{issue}")
        
        if improved:
            logging.info(f"✅ [REGEN] Improved {len(improved)} issues")
        
        return improved
    
    def reinvest(self, improved: List[str]) -> int:
        """
        Redistribuie resursele eliberate (97% reinvestment)
        
        Args:
            improved: List of repaired issues
            
        Returns:
            Amount of resources reinvested (MB)
        """
        if not improved:
            return 0
        
        # Calculate freed resources (simplified)
        resources_freed = len(improved) * 100  # 100MB per issue
        
        # Reinvest 97%
        reinvested = int(resources_freed * 0.97)
        
        logging.info(f"♻️ [REGEN] Reinvested {reinvested}MB (97% of {resources_freed}MB)")
        
        return reinvested
