# src/ai/tool_executioner.py
import logging
from typing import Dict, Any
import json
import random

# Make sure this import is correct for your structure
from src.core.constants import KNOWLEDGE_FILE 

class ToolExecutionError(Exception):
    pass

class ToolExecutor:
    def __init__(self):
        self.tool_definitions = self._load_tool_definitions()
        logging.info("Tool Executor initialized.")

    def _load_tool_definitions(self) -> Dict[str, Any]:
        try:
            with open(KNOWLEDGE_FILE, 'r') as f:
                knowledge = json.load(f)
            return knowledge.get("tool_definitions", {})
        except Exception as e:
            logging.critical(f"FATAL: Could not load tool definitions: {e}")
            return {}

    def execute_action(self, ai_action: str, field_id: str) -> Dict[str, Any]:
        """
        Executes a simulated action and returns a result dictionary
        with 'success', 'cost', and 'tool_id'.
        """
        action_name = ai_action.replace("ACTION: ", "")
        
        if action_name not in self.tool_definitions:
            logging.warning(f"Attempted to execute unknown action: {action_name}")
            raise ToolExecutionError(f"Unknown AI Action: {action_name}")

        tool_details = self.tool_definitions[action_name]
        tool_id = tool_details.get("tool_id")
        cost = tool_details.get("cost", 0)

        # --- NEW SIMULATED FEEDBACK ---
        # Simulate that actions sometimes fail (e.g., pump is clogged)
        # We give "MONITOR" actions a 100% success rate
        # We give other actions a 90% success rate
        
        is_monitoring_action = "MONITOR" in action_name or "LOG" in action_name
        
        # Simulate a 10% failure rate for physical tools
        if not is_monitoring_action and random.random() < 0.1:
            success = False
            message = f"Tool {tool_id} ({action_name}) reported a failure."
            logging.error(f"EXECUTION FAILED: Field {field_id} | {message}")
        else:
            success = True
            message = f"Tool {tool_id} ({action_name}) executed successfully."
            logging.critical(f"EXECUTION: Field {field_id} | {message}")
        
        return {
            "tool_id": tool_id,
            "cost": cost,
            "success": success,
            "message": message,
            "rule_id": ai_action # Pass this back for the heuristic engine
        }