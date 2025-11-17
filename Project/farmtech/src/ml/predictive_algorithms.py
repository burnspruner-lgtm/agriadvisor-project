from typing import Dict, Any

def get_algorithm_details(name: str) -> Dict[str, Any]:
    """Provides metadata for different specialized crop prediction algorithms."""
    algorithms = {
        "LSTM_Sequential": {
            "purpose": "Time series prediction of yield based on soil dynamics.",
            "complexity": "High",
            "required_features": 6
        },
        "RandomForest_Anomaly": {
            "purpose": "Classification of sensor data as normal or anomalous.",
            "complexity": "Medium",
            "required_features": 5
        },
        "Bayesian_Decision": {
            "purpose": "Probabilistic decision making under uncertainty (e.g., weather).",
            "complexity": "High",
            "required_features": 4
        }
    }
    return algorithms.get(name, {"purpose": "Unknown Algorithm", "complexity": "N/A"})

def run_basic_regression(data: Dict[str, Any]) -> float:
    """A simplified linear regression for immediate moisture/temp correlation."""
    moisture_weight = 0.5
    temp_weight = -0.3
    
    # Predicts "risk_score" where higher is worse
    risk_score = (data.get('temp', 0) * temp_weight) + (data.get('moisture', 0) * moisture_weight)
    
    return round(risk_score, 2)