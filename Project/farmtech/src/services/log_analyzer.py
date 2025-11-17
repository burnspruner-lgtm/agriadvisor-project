import logging
import time
import os
from constants import SCHEDULER_LOOP_INTERVAL
from alert_manager import AlertManager

class LogAnalyzer:
    """Background service to detect critical anomalies in system logs."""
    
    def __init__(self, log_file: str = "farm_agent.log"):
        self.log_file = log_file
        self.last_read_position = 0
        self.alert_manager = AlertManager()
        logging.info("Log Analyzer initialized.")

    def analyze_new_logs(self):
        """Reads new log entries and checks for critical phrases."""
        try:
            with open(self.log_file, 'r') as f:
                f.seek(self.last_read_position)
                new_logs = f.readlines()
                self.last_read_position = f.tell()
                
                for line in new_logs:
                    if "FATAL KNOWLEDGE LOAD ERROR" in line:
                        self.alert_manager.send_alert("CRITICAL", "Knowledge Base Load Failure", line)
                    elif "Flow 2.1: CRITICAL CONFLICT" in line:
                         self.alert_manager.send_alert("HIGH", "Autonomy Conflict Triggered", line)
                    elif "RESOURCE SEIZURE" in line or "PRIVILEGE ESCALATION" in line:
                         self.alert_manager.send_alert("CRITICAL_SECURITY", "Privilege Escalation Detected!", line)
                         
        except FileNotFoundError:
            logging.error(f"Log file {self.log_file} not found.")
        except Exception as e:
            logging.error(f"Error during log analysis: {e}")

    def run_analyzer_loop(self):
        """The perpetual loop for log analysis."""
        logging.info("Starting Log Analyzer loop.")
        while True:
            self.analyze_new_logs()
            time.sleep(SCHEDULER_LOOP_INTERVAL * 2) # Check less frequently