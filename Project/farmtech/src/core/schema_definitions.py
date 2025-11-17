# src/core/schema_definitions.py
from typing import Dict, Any

# The definitive schema definition, used by the AI and API
# --- NEW FIELDS ADDED ---
SENSOR_DATA_SCHEMA: Dict[str, Any] = {
    "field_id": str,
    "moisture": int,
    "temp": int,
    "nutrient_level": str,
    "cost_kes": int,
    "pump_pressure": int,
    "historical_trend": str,
    "wind_speed": int,       # <-- NEW
    "solar_radiation": int   # <-- NEW
}

# --- NEW: Dropdown options for the user-friendly UI ---
NUTRIENT_LEVELS: Dict[str, str] = {
    "LOW": "Low nutrient concentration.",
    "OPTIMAL": "Nutrient concentration is optimal.",
    "HIGH": "High nutrient concentration.",
    "N/A": "Sensor data unavailable."
}

HISTORICAL_TRENDS: Dict[str, str] = {
    "NORMAL": "Normal operational history.",
    "HIGH_INTERVENTION": "Frequent past maintenance logs."
}
# --- END NEW ---


def is_valid_schema(data: Dict[str, Any]) -> bool:
    """Checks if a dictionary conforms to the SENSOR_DATA_SCHEMA."""
    for field, expected_type in SENSOR_DATA_SCHEMA.items():
        if field not in data:
            # Allow new fields to be optional for now
            if field in ['wind_speed', 'solar_radiation']:
                data[field] = 0 # Default value
            else:
                logging.warning(f"Schema Validation Failed: Missing key {field}")
                return False
        
        if not isinstance(data.get(field), expected_type):
            logging.warning(f"Schema Validation Failed: Key {field} has wrong type. Expected {expected_type}, got {type(data.get(field))}")
            return False
            
    # Basic range checks
    if not (0 <= data['moisture'] <= 100): return False
    if not (0 <= data['temp'] <= 50): return False
    
    return True

import logging # Make sure logging is imported