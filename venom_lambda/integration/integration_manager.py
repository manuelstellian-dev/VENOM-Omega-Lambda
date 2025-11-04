"""
Integration Manager for VENOM Ω ↔ Λ Communication

This module coordinates bidirectional communication between:
- Ω-AIOS Layer (Kotlin/Android)
- Λ-GENESIS Layer (Python)

Communication Protocols:
1. JSON-RPC over HTTP/REST
2. gRPC for high-performance calls
3. Shared memory for local IPC
"""

import json
import logging
import threading
import time
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class MessageType(Enum):
    """Types of messages exchanged between Ω and Λ"""
    HEALTH_CHECK = "health_check"
    THETA_UPDATE = "theta_update"
    LAMBDA_REQUEST = "lambda_request"
    LAMBDA_RESPONSE = "lambda_response"
    TIME_WRAP_REQUEST = "time_wrap_request"
    TIME_WRAP_RESULT = "time_wrap_result"
    THREAT_ALERT = "threat_alert"
    RESOURCE_UPDATE = "resource_update"


@dataclass
class OmegaHealth:
    """Health metrics from Ω-AIOS"""
    theta: float
    cpu_usage: float
    memory_usage: float
    thermal_state: float
    battery_level: float
    timestamp: float


@dataclass
class LambdaRequest:
    """Request from Ω to Λ for time-wrapped execution"""
    task_id: str
    function_name: str
    parameters: Dict[str, Any]
    priority: int
    timeout: float


@dataclass
class LambdaResponse:
    """Response from Λ to Ω after execution"""
    task_id: str
    success: bool
    result: Any
    lambda_factor: float
    actual_time: float
    compressed_time: float
    error: Optional[str]


class IntegrationManager:
    """
    Manages Ω ↔ Λ Integration
    
    Responsibilities:
    - Serialize/deserialize messages
    - Route messages between layers
    - Monitor communication health
    - Handle failures gracefully
    """
    
    def __init__(self, omega_endpoint: str = "http://localhost:8080",
                 lambda_endpoint: str = "http://localhost:8000"):
        self.omega_endpoint = omega_endpoint
        self.lambda_endpoint = lambda_endpoint
        
        # Message queues
        self.omega_to_lambda_queue = []
        self.lambda_to_omega_queue = []
        
        # Locks for thread safety
        self.omega_lock = threading.Lock()
        self.lambda_lock = threading.Lock()
        
        # Callbacks
        self.message_handlers: Dict[MessageType, Callable] = {}
        
        # Statistics
        self.messages_sent = 0
        self.messages_received = 0
        self.errors = 0
        
        # Health monitoring
        self.last_omega_heartbeat = 0.0
        self.last_lambda_heartbeat = 0.0
        
        logger.info("IntegrationManager initialized")
        logger.info(f"  Ω endpoint: {omega_endpoint}")
        logger.info(f"  Λ endpoint: {lambda_endpoint}")
    
    def register_handler(self, msg_type: MessageType, handler: Callable):
        """Register a message handler"""
        self.message_handlers[msg_type] = handler
        logger.debug(f"Registered handler for {msg_type.value}")
    
    def send_to_lambda(self, message: Dict[str, Any]) -> bool:
        """
        Send message from Ω to Λ
        
        Args:
            message: Message dictionary
            
        Returns:
            True if sent successfully
        """
        try:
            with self.omega_lock:
                self.omega_to_lambda_queue.append({
                    "timestamp": time.time(),
                    "message": message
                })
                self.messages_sent += 1
                logger.debug(f"Queued message to Λ: {message.get('type')}")
                return True
        except Exception as e:
            logger.error(f"Error sending to Λ: {e}")
            self.errors += 1
            return False
    
    def send_to_omega(self, message: Dict[str, Any]) -> bool:
        """
        Send message from Λ to Ω
        
        Args:
            message: Message dictionary
            
        Returns:
            True if sent successfully
        """
        try:
            with self.lambda_lock:
                self.lambda_to_omega_queue.append({
                    "timestamp": time.time(),
                    "message": message
                })
                self.messages_sent += 1
                logger.debug(f"Queued message to Ω: {message.get('type')}")
                return True
        except Exception as e:
            logger.error(f"Error sending to Ω: {e}")
            self.errors += 1
            return False
    
    def collect_omega_health(self, health: OmegaHealth) -> Dict[str, Any]:
        """
        Collect health metrics from Ω-AIOS
        
        Args:
            health: OmegaHealth dataclass
            
        Returns:
            Serialized health data
        """
        health_data = {
            "type": MessageType.HEALTH_CHECK.value,
            "theta": health.theta,
            "cpu_usage": health.cpu_usage,
            "memory_usage": health.memory_usage,
            "thermal_state": health.thermal_state,
            "battery_level": health.battery_level,
            "timestamp": health.timestamp
        }
        
        self.last_omega_heartbeat = time.time()
        logger.debug(f"Collected Ω health: θ={health.theta:.3f}")
        
        return health_data
    
    def create_lambda_request(self, task_id: str, function_name: str,
                            parameters: Dict[str, Any], priority: int = 5,
                            timeout: float = 30.0) -> Dict[str, Any]:
        """
        Create a Lambda execution request
        
        Args:
            task_id: Unique task identifier
            function_name: Name of function to execute
            parameters: Function parameters
            priority: Execution priority (1-10)
            timeout: Maximum execution time
            
        Returns:
            Serialized Lambda request
        """
        request = {
            "type": MessageType.LAMBDA_REQUEST.value,
            "task_id": task_id,
            "function_name": function_name,
            "parameters": parameters,
            "priority": priority,
            "timeout": timeout,
            "timestamp": time.time()
        }
        
        logger.info(f"Created Λ request: {task_id} - {function_name}")
        return request
    
    def process_lambda_response(self, response_data: Dict[str, Any]) -> LambdaResponse:
        """
        Process Lambda execution response
        
        Args:
            response_data: Raw response dictionary
            
        Returns:
            LambdaResponse dataclass
        """
        response = LambdaResponse(
            task_id=response_data.get("task_id", "unknown"),
            success=response_data.get("success", False),
            result=response_data.get("result"),
            lambda_factor=response_data.get("lambda_factor", 1.0),
            actual_time=response_data.get("actual_time", 0.0),
            compressed_time=response_data.get("compressed_time", 0.0),
            error=response_data.get("error")
        )
        
        self.last_lambda_heartbeat = time.time()
        
        if response.success:
            speedup = response.actual_time / response.compressed_time if response.compressed_time > 0 else 1.0
            logger.info(f"Λ response: {response.task_id} - Success (λ={response.lambda_factor:.2f}, speedup={speedup:.2f}x)")
        else:
            logger.error(f"Λ response: {response.task_id} - Failed: {response.error}")
        
        return response
    
    def process_message_queue(self):
        """Process pending messages in queues"""
        # Process Ω → Λ messages
        with self.omega_lock:
            while self.omega_to_lambda_queue:
                item = self.omega_to_lambda_queue.pop(0)
                message = item["message"]
                msg_type = MessageType(message.get("type"))
                
                if msg_type in self.message_handlers:
                    try:
                        self.message_handlers[msg_type](message)
                        self.messages_received += 1
                    except Exception as e:
                        logger.error(f"Error handling message {msg_type}: {e}")
                        self.errors += 1
        
        # Process Λ → Ω messages
        with self.lambda_lock:
            while self.lambda_to_omega_queue:
                item = self.lambda_to_omega_queue.pop(0)
                message = item["message"]
                msg_type = MessageType(message.get("type"))
                
                if msg_type in self.message_handlers:
                    try:
                        self.message_handlers[msg_type](message)
                        self.messages_received += 1
                    except Exception as e:
                        logger.error(f"Error handling message {msg_type}: {e}")
                        self.errors += 1
    
    def check_health(self) -> Dict[str, Any]:
        """
        Check integration health
        
        Returns:
            Health status dictionary
        """
        now = time.time()
        omega_healthy = (now - self.last_omega_heartbeat) < 10.0
        lambda_healthy = (now - self.last_lambda_heartbeat) < 10.0
        
        health = {
            "healthy": omega_healthy and lambda_healthy,
            "omega_healthy": omega_healthy,
            "lambda_healthy": lambda_healthy,
            "omega_last_seen": now - self.last_omega_heartbeat,
            "lambda_last_seen": now - self.last_lambda_heartbeat,
            "messages_sent": self.messages_sent,
            "messages_received": self.messages_received,
            "errors": self.errors,
            "omega_queue_size": len(self.omega_to_lambda_queue),
            "lambda_queue_size": len(self.lambda_to_omega_queue)
        }
        
        return health
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get communication statistics"""
        return {
            "messages_sent": self.messages_sent,
            "messages_received": self.messages_received,
            "errors": self.errors,
            "error_rate": self.errors / max(self.messages_sent, 1),
            "omega_queue_size": len(self.omega_to_lambda_queue),
            "lambda_queue_size": len(self.lambda_to_omega_queue)
        }


# Global instance
_integration_manager: Optional[IntegrationManager] = None


def get_integration_manager() -> IntegrationManager:
    """Get or create global IntegrationManager instance"""
    global _integration_manager
    if _integration_manager is None:
        _integration_manager = IntegrationManager()
    return _integration_manager


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.DEBUG)
    
    manager = IntegrationManager()
    
    # Simulate Ω health update
    health = OmegaHealth(
        theta=0.75,
        cpu_usage=45.2,
        memory_usage=62.8,
        thermal_state=0.3,
        battery_level=87.0,
        timestamp=time.time()
    )
    
    health_msg = manager.collect_omega_health(health)
    manager.send_to_lambda(health_msg)
    
    # Simulate Lambda request
    request = manager.create_lambda_request(
        task_id="task_001",
        function_name="optimize_neural_network",
        parameters={"model": "llama", "iterations": 100},
        priority=8
    )
    
    manager.send_to_lambda(request)
    
    # Check statistics
    stats = manager.get_statistics()
    print(f"\nStatistics: {json.dumps(stats, indent=2)}")
    
    # Check health
    health_status = manager.check_health()
    print(f"\nHealth: {json.dumps(health_status, indent=2)}")
