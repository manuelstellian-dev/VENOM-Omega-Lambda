"""
ENTROPY Organ (E: 15%) - Imunitate și Adaptare
Flow: Self-Attack  Detect  Defend  Learn
"""

import logging
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO)

class EntropyCore:
    """
    Organ ENTROPY - Imunitate și Adaptare
    Testează propriile apărări și învață din amenințări
    """
    
    def __init__(self, genome: Dict[str, Any]):
        self.genome = genome
        self.weight = genome['weights']['E']  # 0.15
        self.learned_threats = []
        self.defense_count = 0
        
        logging.info(f"🛡️ ENTROPY Core initialized (weight: {self.weight})")
    
    def cycle(self, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ciclu imunitar
        
        Args:
            health_data: System health metrics
            
        Returns:
            Dict with cycle results
        """
        # SELF-ATTACK: Testează propriile apărări
        vulnerabilities = self.self_attack()
        
        # DETECT: Detectează amenințări
        threats = self.detect_threats(health_data)
        
        # DEFEND: Apără sistemul
        defended = self.defend(threats)
        
        # LEARN: Învață din amenințări
        self.learn(threats)
        
        self.defense_count += defended
        
        return {
            "organ": "ENTROPY",
            "action": "defending",
            "vulnerabilities": len(vulnerabilities),
            "threats_detected": len(threats),
            "defended": defended,
            "learned": len(self.learned_threats),
            "total_defenses": self.defense_count
        }
    
    def self_attack(self) -> List[str]:
        """
        Testează propriile apărări (ca un sistem imunitar)
        
        Returns:
            List of detected vulnerabilities
        """
        test_attacks = [
            "memory_overflow",
            "cpu_spike",
            "model_poisoning",
            "cache_corruption"
        ]
        
        vulnerabilities = []
        
        for attack in test_attacks:
            if not self.is_defended_against(attack):
                vulnerabilities.append(attack)
                logging.warning(f"🔍 [ENTROPY] Vulnerability found: {attack}")
        
        if not vulnerabilities:
            logging.debug(f"✅ [ENTROPY] Self-attack: all defenses intact")
        
        return vulnerabilities
    
    def detect_threats(self, health_data: Dict[str, Any]) -> List[str]:
        """
        Detectează amenințări reale
        
        Args:
            health_data: System health metrics
            
        Returns:
            List of detected threats
        """
        threats = []
        
        # CPU spike anomaly
        cpu_health = health_data.get('cpu_health', 1.0)
        if cpu_health < 0.1:
            threats.append("cpu_spike")
            logging.warning(f"⚠️ [ENTROPY] Threat detected: cpu_spike (health: {cpu_health:.2f})")
        
        # Memory anomaly
        memory_health = health_data.get('memory_health', 1.0)
        if memory_health < 0.2:
            threats.append("memory_attack")
            logging.warning(f"⚠️ [ENTROPY] Threat detected: memory_attack (health: {memory_health:.2f})")
        
        # Thermal attack (sustained overheating)
        thermal_health = health_data.get('thermal_health', 1.0)
        if thermal_health < 0.3:
            threats.append("thermal_attack")
            logging.warning(f"⚠️ [ENTROPY] Threat detected: thermal_attack (health: {thermal_health:.2f})")
        
        return threats
    
    def defend(self, threats: List[str]) -> int:
        """
        Apără împotriva amenințărilor
        
        Args:
            threats: List of detected threats
            
        Returns:
            Number of threats defended
        """
        defended_count = 0
        
        for threat in threats:
            if threat in self.learned_threats:
                # Known threat - effective defense
                logging.info(f"🛡️ [ENTROPY] Defended (known): {threat}")
                defended_count += 1
            else:
                # New threat - partial defense
                logging.info(f"🛡️ [ENTROPY] Defended (learning): {threat}")
                defended_count += 0.5
        
        return int(defended_count)
    
    def learn(self, threats: List[str]):
        """
        Învață din amenințări noi
        
        Args:
            threats: List of threats to learn from
        """
        for threat in threats:
            if threat not in self.learned_threats:
                self.learned_threats.append(threat)
                logging.info(f"🧠 [ENTROPY] Learned new threat: {threat}")
        
        # Keep only last 100 threats
        if len(self.learned_threats) > 100:
            self.learned_threats = self.learned_threats[-100:]
    
    def is_defended_against(self, attack: str) -> bool:
        """
        Verifică dacă e apărat împotriva unui atac
        
        Args:
            attack: Attack type
            
        Returns:
            True if defended
        """
        return attack in self.learned_threats
