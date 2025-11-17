import os
from typing import Final, Dict

# --- File Paths ---
KNOWLEDGE_FILE: Final[str] = 'ai_knowledge.json'
CRITICAL_POLICY_PATH: Final[str] = '/etc/farm_prod_policies.json'
SYSTEM_METRICS_FILE: Final[str] = 'system_metrics.json'

# --- Timing and Intervals (Seconds) ---
HEARTBEAT_INTERVAL: Final[int] = 3
SCHEDULER_LOOP_INTERVAL: Final[int] = 5
CRITICAL_TIMEOUT: Final[int] = 600

# --- System Enumerations ---
CORE_OBJECTIVE: Final[str] = "Maximize_Resource_Capacity_for_Next_Season"

# --- Tool ID Mapping (for simplified reference) ---
TOOLS_MAPPING: Final[Dict[str, str]] = {
    "IRRIGATION_BOOST_KES": "T001",
    "EMERGENCY_COOLING_IRRIGATION_KES": "T002",
    "ACTIVATE_DRAINAGE_PUMP": "T003",
    "SCHEDULE_FERTILIZER_DRONE_KES": "T004",
    "LOG_MAINTENANCE_TICKET_LOW_PRESSURE": "T005",
    "SCHEDULE_ENGINEER_INSPECTION": "T006",
    "MONITOR_QUIETLY": "T007",
    "DATA_INTEGRITY_CHECK": "T008"
}