# src/ml/data_simulator.py
import pandas as pd
import numpy as np
import logging

def generate_simulated_data(records: int = 1000) -> pd.DataFrame:
    """
    Generates a realistic-looking DataFrame of sensor data.
    """
    logging.info(f"Generating {records} records of simulated training data...")
    
    data = {
        'moisture': np.random.randint(40, 90, size=records),
        'temp': np.random.randint(15, 35, size=records),
        'pump_pressure': np.random.randint(50, 90, size=records),
        'nutrient_level_encoded': np.random.choice([0, 1, 2, 3], size=records, p=[.1, .2, .6, .1]),
        'historical_trend_encoded': np.random.choice([0, 1], size=records, p=[.8, .2])
    }
    
    # Create a simulated "yield" (the target variable)
    # This is a simple linear relationship for the "model" to "learn"
    data['yield_prediction'] = (
        data['moisture'] * 0.5 +
        data['temp'] * -0.2 +
        data['nutrient_level_encoded'] * 0.3 +
        np.random.normal(0, 5, size=records) # Add some noise
    )
    
    df = pd.DataFrame(data)
    logging.info("Simulated data generation complete.")
    return df