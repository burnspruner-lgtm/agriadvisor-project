from typing import Dict, List, Any

# Simple dataclasses/type definitions to enforce API contract integrity

class SensorDataInput:
    """Defines the strict schema for incoming sensor data."""
    SCHEMA: Dict[str, Any] = {
        "field_id": str,
        "moisture": int,
        "temp": int,
        "nutrient_level": str,
        "cost_kes": int,
        "pump_pressure": int,
        "historical_trend": str
    }

class PredictionResponse:
    """Defines the structure for the model's output."""
    def __init__(self, prediction: str, confidence: float):
        self.prediction = prediction
        self.confidence = confidence

    def to_dict(self) -> Dict[str, Any]:
        return {"prediction": self.prediction, "confidence": self.confidence}

class DecisionResponse:
    """Defines the final response structure for the /process_data endpoint."""
    def __init__(self, prediction: str, ai_action: str, safety_lock_active: bool):
        self.status = "success"
        self.prediction = prediction
        self.ai_action = ai_action
        self.safety_lock_active = safety_lock_active

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "prediction": self.prediction,
            "ai_action": self.ai_action,
            "safety_lock_active": self.safety_lock_active
        }