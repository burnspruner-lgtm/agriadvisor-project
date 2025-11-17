import logging
import datetime
from typing import Dict, Any

class AlertManager:
    """Handles formatting and routing of critical system alerts."""

    def __init__(self, primary_contact: str = "engineer@dekut.io"):
        self.primary_contact = primary_contact
        logging.info(f"Alert Manager initialized. Primary contact: {self.primary_contact}")

    def _format_message(self, severity: str, title: str, details: str) -> Dict[str, str]:
        """Creates a standardized alert dictionary."""
        timestamp = datetime.datetime.now().isoformat()
        return {
            "timestamp": timestamp,
            "severity": severity,
            "title": title,
            "details": details,
            "recipient": self.primary_contact
        }

    def send_alert(self, severity: str, title: str, details: str):
        """
        Simulates sending an alert (e.g., via email, SMS, or monitoring system).
        """
        alert_data = self._format_message(severity, title, details)

        if severity in ["CRITICAL", "CRITICAL_SECURITY"]:
            logging.critical(f"!! ALERT SENT !! [{severity}] {title} to {self.primary_contact}")
            # In production, this would call an external API (e.g., Twilio, PagerDuty)
        elif severity == "HIGH":
            logging.error(f"! ALERT LOGGED ! [{severity}] {title}")
        else:
            logging.warning(f"[INFO] Alert logged: {title}")

        # Log the full alert data to a separate alerts log (simulated)
        # print(f"ALERT_DATA: {alert_data}")
        return alert_data