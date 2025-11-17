# src/ml/model_training.py
import logging
import time
import json
import os
from src.ml.data_simulator import generate_simulated_data
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# --- NEW CONFIG ---
MODEL_FEATURES = [
    'moisture', 'temp', 'pump_pressure', 
    'nutrient_level_encoded', 'historical_trend_encoded'
]
TARGET_VARIABLE = 'yield_prediction'
MODEL_SAVE_FILE = 'simulated_model_v1.json' # This is the "trained" model

def train_new_model():
    """
    Simulates a full end-to-end training and validation pipeline.
    This script replaces the old, simple simulation.
    """
    logging.info("--- STARTING NEW ML MODEL TRAINING PIPELINE ---")
    
    # 1. Load Data
    data = generate_simulated_data(records=2000)
    
    # 2. Split Data
    X = data[MODEL_FEATURES]
    y = data[TARGET_VARIABLE]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 3. Simulate Training
    logging.info(f"Training LinearRegression model on {len(X_train)} records...")
    model = LinearRegression()
    start_time = time.time()
    model.fit(X_train, y_train)
    train_time = time.time() - start_time
    logging.info(f"Training complete in {train_time:.2f}s.")
    
    # 4. Evaluate and Save
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    model_metadata = {
        "model_name": "SimulatedLinearRegression-v1.0",
        "last_trained": time.time(),
        "training_time_sec": train_time,
        "records_trained": len(X_train),
        "performance_metrics": {
            "mae": mae,
            "r_squared": r2
        },
        "features_used": MODEL_FEATURES
    }
    
    logging.info(f"New Model Performance: MAE: {mae:.2f}, R2: {r2:.2f}")

    # 5. Save the "trained model" metadata
    try:
        with open(MODEL_SAVE_FILE, 'w') as f:
            json.dump(model_metadata, f, indent=4)
        logging.info(f"New model saved to {MODEL_SAVE_FILE}.")
    except Exception as e:
        logging.error(f"Failed to save model file: {e}")
        
    logging.info("--- ML MODEL TRAINING PIPELINE FINISHED ---")

if __name__ == "__main__":
    # This allows you to run "python src/ml/model_training.py"
    # to "train" your model
    train_new_model()