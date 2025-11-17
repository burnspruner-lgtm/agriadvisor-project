# FarmTech Analytics API Documentation (V6.0)

Base URL: `http://127.0.0.1:5000`

## 1. POST /process_data

The primary endpoint for submitting new sensor data for processing, prediction, and action decision.

| Field | Type | Description | Required | Example |
| :--- | :--- | :--- | :--- | :--- |
| **field_id** | `string` | Unique identifier for the crop field. | Yes | "A-47-Wheat" |
| **moisture** | `integer` | Soil moisture level (0-100%). | Yes | 65 |
| **temp** | `integer` | Ambient temperature (°C). | Yes | 25 |
| **nutrient_level** | `string` | Nutrient status: LOW, OPTIMAL, HIGH, N/A. | Yes | "OPTIMAL" |
| **cost_kes** | `integer` | Estimated cost of the most recent action (KES). | Yes | 10000 |
| **pump_pressure** | `integer` | Water pump pressure (psi). | Yes | 70 |
| **historical_trend** | `string` | Past stability: NORMAL or HIGH_INTERVENTION. | Yes | "NORMAL" |

### Example Request

```json
[
    {
        "field_id": "A-47-Wheat", 
        "moisture": 65,
        "nutrient_level": "OPTIMAL",
        "temp": 25,
        "cost_kes": 10000, 
        "pump_pressure": 70,
        "historical_trend": "NORMAL"
    }
]