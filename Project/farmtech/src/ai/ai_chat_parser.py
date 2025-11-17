# src/ai/ai_chat_parser.py
import logging
from typing import Dict, Any

# --- NEW: We must import the AI classes to query them ---
# (Adjust these imports if your file structure is different)
try:
    from src.ai.ai_agent import AIActionDecider, ai_agent_status
    from src.ai.heuristic_engine import HeuristicEngine
except ImportError:
    logging.critical("Chat Parser: Could not import AI components!")
    # Define dummy classes if import fails, so the app can still run
    class AIActionDecider: pass
    class HeuristicEngine: pass
    ai_agent_status = {}


# Store last decision for "why" questions
last_decision_context = "No decision has been made yet."

def update_last_decision(context: str):
    """Called by the gateway to update the chat parser's memory."""
    global last_decision_context
    last_decision_context = context

def parse_ai_query(query: str, ai_agent: AIActionDecider, heuristic_engine: HeuristicEngine) -> str:
    """
    Parses a natural language query from the user and returns an intelligent response.
    This is the core of the "interactive" AI.
    """
    query = query.lower().strip()
    logging.info(f"Parsing AI Chat Query: '{query}'")

    try:
        # --- Rule 1: "explain [rule]" ---
        if "explain" in query and "r0" in query:
            rule_id = query.split(" ")[-1].upper() # Gets 'R006'
            if not hasattr(ai_agent, 'rules'):
                return "AI agent is not fully initialized. Cannot explain rules yet."
                
            for rule in ai_agent.rules:
                if rule['id'] == rule_id:
                    return f"Rule {rule_id} is: '{rule['log']}' It has a priority of {rule.get('priority', 'N/A')}."
            return f"Sorry, I don't have a rule named {rule_id} in my knowledge base."

        # --- Rule 2: "confidence in [tool]" ---
        if "confidence" in query:
            if not hasattr(heuristic_engine, 'heuristics'):
                return "Heuristic engine is not initialized. Cannot get confidence yet."

            if "irrigation" in query:
                rule_id = "R006_STANDARD_IRRIGATION" # Example rule
            elif "cooling" in query:
                rule_id = "R001_EMERGENCY_COOLING_IRRIGATION_KES" # Example rule
            else:
                return "Which tool's confidence are you asking about? (e.g., 'irrigation', 'cooling')"
            
            # Get the *average* confidence for this rule across all fields
            scores = [v['confidence'] for k, v in heuristic_engine.heuristics.items() if rule_id in k]
            if not scores:
                return f"I have no learning data for {rule_id} yet. My default confidence is 100%."
            
            avg_score = (sum(scores) / len(scores)) * 100
            return f"My current learned confidence for rule {rule_id} is {avg_score:.1f}%."

        # --- Rule 3: "status of [field]" ---
        if "status of" in query:
            field_id = query.split("status of")[-1].strip()
            # This is a simulation; a real app would query the DB
            return (f"I'm actively monitoring {field_id}. All sensors appear to be stable. "
                    f"The last action taken was '{ai_agent_status.get('last_action', 'N/A')}'.")

        # --- Rule 4: "why did you" ---
        if "why" in query:
            return f"My last major decision was based on this context: {last_decision_context}"
        
        # --- Rule 5: "hello" / "who are you" ---
        if "hello" in query or "who are you" in query:
            return ("Hello! I am Agriadvisor, a Heuristic AI. "
                    "I make rational decisions for the farm and learn from their outcomes.")
        
        # --- Fallback ---
        return "Sorry, I don't understand that question. Try asking me to 'explain R001' or 'what is your confidence in irrigation?'"

    except Exception as e:
        logging.error(f"Error parsing chat query: {e}")
        return "I encountered an error trying to process that."