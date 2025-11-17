import logging
from typing import Dict, Any
from db_connector import DBConnector
from ai_agent import AgentContext # Assuming we need access to the context thresholds

class CostManager:
    """Logic for financial tracking, budget adherence, and calculating cost projections."""
    
    def __init__(self, agent_context: AgentContext):
        self.cost_limit_kes = agent_context.cost_limit
        logging.info(f"Cost Manager initialized. Daily Action Limit: KES {self.cost_limit_kes}")

    def is_within_budget(self, proposed_cost: int) -> bool:
        """Checks if a proposed action cost is below the configured critical limit."""
        if proposed_cost > self.cost_limit_kes:
            logging.warning(f"Cost breach: Proposed cost KES {proposed_cost} exceeds limit KES {self.cost_limit_kes}.")
            return False
        return True

    def log_action_cost(self, field_id: str, action_type: str, cost: int):
        """Logs the final executed cost into the database for financial tracking."""
        query = "INSERT INTO cost_log (field_id, action_type, cost, timestamp) VALUES (?, ?, ?, datetime('now'))"
        success = DBConnector.execute_commit(query, (field_id, action_type, cost))
        
        if success:
            logging.info(f"Cost KES {cost} logged for action {action_type} on {field_id}.")
        else:
            logging.error("Failed to log action cost to database.")
        
        # Note: A new table 'cost_log' is implicitly required here.