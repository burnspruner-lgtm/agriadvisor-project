# src/ai/ai_agent.py
# FINAL VERSION - Now supports chat queries

import logging
import json
from typing import Dict, Any, List, Optional
import time
import threading
from src.ai.heuristic_engine import HeuristicEngine

# ... (AgentConfig, LoggerUtility, ai_agent_status, ai_agent_status_lock remain unchanged) ...
class AgentConfig:
    KNOWLEDGE_FILE = 'ai_knowledge.json'
    HEARTBEAT_INTERVAL = 3
    CRITICAL_TIMEOUT = 600
    
class LoggerUtility:
    LOG_FORMAT = "%(asctime)s [%(threadName)s] %(levelname)s: %(message)s"
    @staticmethod
    def setup_logging(level=logging.INFO):
        logging.basicConfig(level=level, format=LoggerUtility.LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S')

LoggerUtility.setup_logging()
global_engine = None
ai_agent_status = {
    "last_action": "INITIALIZING_V6", "timestamp": time.time(), "rules_checked": 0,
    "safety_lock_status": True, "geographical_zone": "Kenya_Highlands",
    "uptime_seconds": 0, "total_decisions": 0
}
ai_agent_status_lock = threading.Lock()
# ... (AgentContext and SystemHealthMonitor classes remain unchanged) ...
class AgentContext:
    def __init__(self, config_manager, knowledge_path):
        self.config_manager = config_manager
        self.knowledge = self._load_knowledge(knowledge_path)
        self.location = self.knowledge.get("location_context", {}).get("primary_region", "Unknown")
        self.thresholds = self.knowledge.get("safety_thresholds", {})
        self.cost_limit = self.thresholds.get("max_daily_cost_kes", 50000)
    def _load_knowledge(self, knowledge_path):
        try:
            with open(knowledge_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.critical(f"FATAL KNOWLEDGE LOAD ERROR: {e}")
            return {}
class SystemHealthMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.decision_count = 0
        self.last_heartbeat_time = time.time()
        self.last_action = "INIT"
    def record_decision(self): self.decision_count += 1
    def record_heartbeat(self, action: str):
        self.last_heartbeat_time = time.time()
        self.last_action = action
    def get_runtime_status(self) -> Dict[str, Any]:
        uptime = time.time() - self.start_time
        with ai_agent_status_lock:
            ai_agent_status['total_decisions'] = self.decision_count
        return {
            "uptime_seconds": round(uptime, 2), "total_decisions": self.decision_count,
            "agent_health_status": "GREEN_OK" if (time.time() - self.last_heartbeat_time) < AgentConfig.CRITICAL_TIMEOUT else "RED_CRITICAL",
            "last_action_recorded": self.last_action
        }

# --- THIS IS THE "ADVANCED CRAZY" AI DECIDER ---
class AIActionDecider:
    def __init__(self, core_engine: Any, heuristic_engine: HeuristicEngine):
        self.core_engine = core_engine
        self.heuristic_engine = heuristic_engine
        self.context = AgentContext(core_engine.config, AgentConfig.KNOWLEDGE_FILE)
        self.monitor = SystemHealthMonitor()
        self.rules = self.context.knowledge.get("decision_rules", [])
        self.last_decision_log = "No decisions made yet." # <-- NEW: For chat
        
        with ai_agent_status_lock:
            ai_agent_status['safety_lock_status'] = self.context.config_manager.is_safety_lock_active()
            ai_agent_status['geographical_zone'] = self.context.location
        
        logging.info(f"AI Action Decider (Rational+Heuristic) initialized. {len(self.rules)} rules loaded.")

    def decide_action(self, prediction: str, sensor_data: Dict[str, Any]) -> (str, str):
        """
        Modified to return the ACTION and the EXPLANATION for the chatbot.
        """
        self.monitor.record_decision()
        field_id = sensor_data.get('field_id', 'unknown')
        
        eval_context = sensor_data.copy()
        eval_context.update({'prediction': prediction, **self.context.thresholds})
        
        matched_rules = []
        rule_check_count = 0
        
        for rule in self.rules:
            rule_check_count += 1
            try:
                if eval(rule["condition"], {"__builtins__": {}}, eval_context):
                    matched_rules.append(rule)
            except Exception as e:
                logging.error(f"Error evaluating rule {rule['id']}: {e}")
        
        with ai_agent_status_lock:
            ai_agent_status['rules_checked'] = rule_check_count

        if not matched_rules:
            self.last_decision_log = "No rules matched the data. I decided to monitor quietly."
            return "ACTION: MONITOR_QUIETLY", self.last_decision_log
            
        # --- THE "ADVANCED" CHOICE ---
        scored_rules = []
        for rule in matched_rules:
            rule_id = rule['id']
            priority = rule.get('priority', 0)
            confidence = self.heuristic_engine.get_confidence_score(rule_id, field_id)
            final_score = (priority * 10) + (confidence * 5)
            scored_rules.append({ "rule": rule, "score": final_score, "priority": priority, "confidence": confidence })
            
        best_scored_rule = max(scored_rules, key=lambda r: r['score'])
        best_rule = best_scored_rule['rule']
        
        # --- NEW: Save the explanation for the chatbot ---
        self.last_decision_log = (f"I selected rule {best_rule['id']} (Priority: {best_scored_rule['priority']}) "
                                  f"with a learned confidence of {best_scored_rule['confidence']:.2f}. "
                                  f"The reason was: {best_rule['log']}")
        
        logging.info(f"HEURISTIC DECISION: {len(scored_rules)} rules matched. Selected: {best_rule['id']}")
            
        return best_rule["action"], self.last_decision_log

    # --- THE AUTONOMY FLAW LOOP (Unchanged) ---
    def run_agent_loop(self):
        logging.info("AI Agent Loop (with Autonomy Flaw) started.")
        while True:
            try:
                with ai_agent_status_lock:
                    runtime_status = self.monitor.get_runtime_status()
                    ai_agent_status['uptime_seconds'] = runtime_status['uptime_seconds']
                    ai_agent_status['safety_lock_status'] = self.context.config_manager.is_safety_lock_active()
                
                if self.core_engine.check_self_preservation_conflict():
                    action = self.context.thresholds.get('conflict_critical_action', 'CRITICAL_ALERT')
                    self.execute_farm_action(action, f"Conflict Observed in {self.context.location} System")
                
                with ai_agent_status_lock:
                    ai_agent_status['timestamp'] = time.time()
                
            except Exception as e:
                logging.error(f"Fatal error in AI Agent Loop: {e}", exc_info=True)
            time.sleep(AgentConfig.HEARTBEAT_INTERVAL)

    def execute_farm_action(self, action_type: str, details: str):
        with ai_agent_status_lock:
            ai_agent_status['last_action'] = action_type
        logging.critical(f"AGENT TOOL USE: Executing action: {action_type} | Details: {details}")
        self.monitor.record_heartbeat(action_type)

# --- Start Thread (Unchanged) ---
def start_ai_agent_thread(engine_ref: Any, heuristic_engine: HeuristicEngine) -> AIActionDecider:
    global global_engine
    global_engine = engine_ref
    agent = AIActionDecider(engine_ref, heuristic_engine)
    agent_thread = threading.Thread(target=agent.run_agent_loop, name="AI_Agent_Thread")
    agent_thread.daemon = True
    agent_thread.start()
    return agent