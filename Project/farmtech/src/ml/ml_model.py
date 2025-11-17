# src/ml/ml_model.py
import logging
from typing import Dict, List, Any
import random
import json

# This is the "trained" model file created by model_training.py
MODEL_FILE = 'simulated_model_v1.json'

class MachineLearningModel:
    """
    Simulates the predictive model.
    It now loads its "metadata" from a trained model file.
    """
    
    def __init__(self):
        self.model_metadata = self._load_trained_model()
        if self.model_metadata:
            logging.info(f"ML Model '{self.model_metadata.get('model_name')}' loaded.")
            logging.info(f"Model Performance: R2: {self.model_metadata['performance_metrics'].get('r_squared', 'N/A')}")
        else:
            logging.error("Failed to load any ML model metadata.")

    def _load_trained_model(self) -> Dict[str, Any]:
        """Loads the 'trained' model's metadata."""
        try:
            with open(MODEL_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Could not load model file {MODEL_FILE}: {e}")
            return None

    def run_prediction(self, feature_vector: List[Dict]) -> str:
        """
        Simulates a prediction based on the input data.
        """
        if not self.model_metadata:
             return "ERROR: Model_Unavailable"

        # Simulate the model's prediction logic
        try:
            moisture = feature_vector[0].get('moisture', 70)
            temp = feature_vector[0].get('temp', 25)
            
            if moisture < 50 and temp > 30:
                return "Critical Drought Warning"
            elif moisture < 65:
                return "Optimal Irrigation Recommended"
            elif moisture > 85:
                return "Waterlogging Risk Detected"
            else:
                return "All Metrics Stable"
                
        except Exception as e:
            logging.error(f"Error during ML prediction: {e}")
            return "ERROR: Prediction_Failed"