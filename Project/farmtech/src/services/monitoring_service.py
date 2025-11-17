import logging
import time
from typing import Dict, Any, Optional
from src.core.constants import SYSTEM_METRICS_FILE
import json
import threading

# Global status dictionary (typically imported from ai_agent.py, but defined here for independence)
# Assuming 'ai_agent_status' and 'SystemHealthMonitor' from ai_agent.py are used

class MonitoringService:
    """Centralized tracking of system health, latency, and decision history."""
    
    def __init__(self, agent_monitor: Any): # Accepts the SystemHealthMonitor instance
        self.agent_monitor = agent_monitor
        self._metrics_history: List[Dict[str, Any]] = []
        logging.info("Monitoring Service initialized.")

    def get_full_agent_status(self) -> Dict[str, Any]:
        """Combines global status and runtime health metrics."""
        
        # --- Simulated global status from ai_agent.py ---
        simulated_ai_agent_status = {
            "last_action": "MONITORING_QUIETLY", 
            "timestamp": time.time(), 
            "rules_checked": 11,
            "safety_lock_status": True,
            "geographical_zone": "Kenya_Highlands"
        }
        
        status = simulated_ai_agent_status.copy()
        
        # Add runtime metrics from the SystemHealthMonitor instance
        if self.agent_monitor:
            status.update(self.agent_monitor.get_runtime_status())
            
        return status

    def log_and_save_metrics(self):
        """Periodically records and saves the system metrics to a file."""
        current_metrics = self.get_full_agent_status()
        current_metrics['log_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self._metrics_history.append(current_metrics)
        
        if len(self._metrics_history) > 1000:
            self._metrics_history.pop(0)

        # Save to JSON file
        try:
            with open(SYSTEM_METRICS_FILE, 'w') as f:
                json.dump(self._metrics_history, f, indent=4)
        except Exception as e:
            logging.error(f"Failed to save system metrics: {e}")
            
        logging.debug("System metrics logged and saved.")