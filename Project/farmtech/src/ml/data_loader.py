# --- CHANGED ---
# import sqlite3 # No longer need this
import logging
from typing import List, Dict, Any
from src.services.db_connector import DBConnector # --- ADDED ---

def load_historical_data(field_id: str, days: int = 30) -> List[Dict[str, Any]]:
    """
    Fetches historical sensor data for training or context
    using the thread-safe DBConnector. (Task 2)
    """
    # DB_NAME = "local_farm_data.db" # --- REMOVED ---
    query = f"""
        SELECT moisture, temp, nutrient_level, pump_pressure, ai_action, timestamp 
        FROM sensor_data 
        WHERE field_id = ? 
        ORDER BY timestamp DESC 
        LIMIT ?
    """
    # conn = None # --- REMOVED ---
    
    # --- CHANGED ---
    # The entire try/except/finally block is replaced
    # with one call to the efficient DBConnector.
    
    historical_data = DBConnector.execute_query(query, (field_id, days))

    if historical_data is None:
        logging.error(f"DBConnector failed to load historical data for {field_id}.")
        return []
    
    logging.info(f"Loaded {len(historical_data)} historical records for {field_id}.")
    return historical_data

    # --- REMOVED ---
    # try:
    #     conn = sqlite3.connect(DB_NAME)
    #     ... (all old logic) ...
    # finally:
    #     if conn:
    #         conn.close()