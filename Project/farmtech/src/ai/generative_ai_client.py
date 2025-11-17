# src/ai/generative_ai_client.py
import google.generativeai as genai
import logging
from typing import Dict, Any

# --- !!! PASTE YOUR API KEY HERE !!! ---
# (Get your key from aistudio.google.com)
YOUR_API_KEY = "PASTE_YOUR_API_KEY_HERE"

class GenerativeAIClient:
    """
    This class replaces the ai_agent.py.
    It calls an external Generative AI (Gemini) instead of using local rules.
    """
    
    def __init__(self):
        try:
            genai.configure(api_key=YOUR_API_KEY)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            logging.info("GenerativeAIClient initialized successfully.")
        except Exception as e:
            logging.error(f"Failed to configure Generative AI. Check API Key? Error: {e}")
            self.model = None

    def get_ai_decision(self, sensor_data: Dict[str, Any], ml_prediction: str) -> str:
        """
        Gets a new, creative decision from the Generative AI.
        """
        if not self.model:
            return "ERROR: GENERATIVE_AI_NOT_INITIALIZED"

        # 1. We create a "prompt" for the AI
        prompt = f"""
        You are 'Agriadvisor', an expert AI for Kenyan agriculture.
        A machine learning model has given a prediction, and you must decide the final, real-world action.

        Here is the data from the farm (in Kenya):
        - Field ID: {sensor_data.get('field_id')}
        - Soil Moisture: {sensor_data.get('moisture')}%
        - Temperature: {sensor_data.get('temp')}°C
        - Nutrient Level: {sensor_data.get('nutrient_level')}
        - Recent Cost (KES): {sensor_data.get('cost_kes')}
        - Pump Pressure: {sensor_data.get('pump_pressure')} psi
        - Historical Trend: {sensor_data.get('historical_trend')}

        The local ML model prediction is: "{ml_prediction}"

        Based on all this, what is the single, best, and safest action to take?
        Be concise. Start your response with 'ACTION:'
        (e.g., ACTION: Boost irrigation, but monitor pump pressure.)
        """

        try:
            # 2. We send the prompt to the AI API
            response = self.model.generate_content(prompt)
            
            # 3. We get the text response back
            ai_action = response.text.strip()
            logging.info(f"Generative AI Decision: {ai_action}")
            return ai_action

        except Exception as e:
            logging.error(f"Error getting AI decision: {e}")
            return f"ERROR: AI_GENERATION_FAILED: {e}"