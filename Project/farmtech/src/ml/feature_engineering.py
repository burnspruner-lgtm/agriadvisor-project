from typing import Dict, Any, List

# Simple mapping for categorical features (should match model_config.json)
NUTRIENT_MAP: Dict[str, int] = {"N/A": 0, "LOW": 1, "OPTIMAL": 2, "HIGH": 3}
TREND_MAP: Dict[str, int] = {"NORMAL": 0, "HIGH_INTERVENTION": 1}

def apply_feature_engineering(raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Transforms raw sensor data into the numerical features required by the ML model.
    """
    processed_data = []
    
    for record in raw_data:
        # 1. Encode Categorical Features
        nutrient_encoded = NUTRIENT_MAP.get(record.get('nutrient_level', 'N/A').upper(), 0)
        trend_encoded = TREND_MAP.get(record.get('historical_trend', 'NORMAL').upper(), 0)
        
        # 2. Calculate Derived Features (e.g., Heat Stress Index)
        moisture = record.get('moisture', 0)
        temp = record.get('temp', 0)
        heat_stress_index = (temp * 0.5) - (moisture * 0.1) 
        
        # 3. Create the final feature vector
        feature_vector = {
            "field_id": record.get('field_id'),
            "moisture": moisture,
            "temp": temp,
            "pump_pressure": record.get('pump_pressure', 0),
            "nutrient_level_encoded": nutrient_encoded,
            "historical_trend_encoded": trend_encoded,
            "heat_stress_index": heat_stress_index
        }
        processed_data.append(feature_vector)
        
    return processed_data