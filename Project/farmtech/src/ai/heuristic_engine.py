# src/ai/heuristic_engine.py
import json
import logging
from typing import Dict, Any

HEURISTIC_FILE = 'dynamic_heuristics.json'
LEARNING_RATE = 0.1
FAILURE_PENALTY = -0.2
SUCCESS_REWARD = 0.1

class HeuristicEngine:
    """
    This is the "Advanced Crazy" AI.
    It learns from the outcomes of actions to build a dynamic
    confidence score for different rules and situations.
    """
    def __init__(self):
        self.heuristics = self._load_heuristics()
        logging.info("Heuristic Engine (Learning AI) initialized.")

    def _load_heuristics(self) -> Dict[str, Any]:
        """Loads the AI's 'memory' from a file."""
        try:
            with open(HEURISTIC_FILE, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            logging.warning(f"Heuristic file '{HEURISTIC_FILE}' not found. Starting with empty memory.")
            return {}

    def _save_heuristics(self):
        """Saves the AI's 'memory' to a file."""
        try:
            with open(HEURISTIC_FILE, 'w') as f:
                json.dump(self.heuristics, f, indent=4)
        except Exception as e:
            logging.error(f"Failed to save heuristics: {e}")

    def get_confidence_score(self, rule_id: str, field_id: str) -> float:
        """
        Gets the AI's learned confidence in a specific rule for a specific field.
        Returns 1.0 (100% confidence) if it has no memory.
        """
        key = f"{rule_id}@{field_id}"
        return self.heuristics.get(key, {}).get("confidence", 1.0)

    def learn_from_feedback(self, rule_id: str, field_id: str, success: bool):
        """
        This is the core learning loop. The AI updates its own confidence.
        """
        key = f"{rule_id}@{field_id}"
        if key not in self.heuristics:
            self.heuristics[key] = {"confidence": 1.0, "successes": 0, "failures": 0}
        
        current_confidence = self.heuristics[key]["confidence"]
        
        if success:
            # Apply reward
            update = SUCCESS_REWARD
            self.heuristics[key]["successes"] += 1
            logging.info(f"HEURISTIC: Rewarding rule {key}. Confidence {current_confidence:.2f} -> {current_confidence + update:.2f}")
        else:
            # Apply penalty
            update = FAILURE_PENALTY
            self.heuristics[key]["failures"] += 1
            logging.warning(f"HEURISTIC: Penalizing rule {key}. Confidence {current_confidence:.2f} -> {current_confidence + update:.2f}")
            
        # Update confidence using a learning rate
        new_confidence = current_confidence + update
        # Clamp confidence between 0.1 (never 0) and 1.0
        self.heuristics[key]["confidence"] = max(0.1, min(1.0, new_confidence))
        
        self._save_heuristics()