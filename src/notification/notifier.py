# notification/notifier.py
import requests
import json
import os
from typing import Optional, Dict, Any
from datetime import datetime


class Notifier:
    """Handles notifications to supervisors and customers."""

    def __init__(self, webhook_url=None):
        """Initialize with optional webhook URL."""
        self.webhook_url = webhook_url or os.environ.get("NOTIFICATION_WEBHOOK_URL")

        # Log of all notifications for simulation and debugging
        self.notification_log = []

    def notify_supervisor(self, request_id: str, message: str):
        """Notify a supervisor about a help request."""
        notification = {
            "type": "supervisor_notification",
            "request_id": request_id,
            "message": message,
            "timestamp": datetime.now().isoformat(),
        }

        # Log notification
        self.notification_log.append(notification)

        # Console simulation
        print(f"\n[SUPERVISOR NOTIFICATION] Request ID: {request_id}")
        print(f"Message: {message}")

        # Send webhook if configured
        self._send_webhook(notification)

    def notify_customer(self, customer_id: str, message: str):
        """Notify a customer with a response."""
        notification = {
            "type": "customer_notification",
            "customer_id": customer_id,
            "message": message,
            "timestamp": datetime.now().isoformat(),
        }

        # Log notification
        self.notification_log.append(notification)

        # Console simulation
        print(f"\n[CUSTOMER NOTIFICATION] Customer ID: {customer_id}")
        print(f"Message: {message}")

        # Send webhook if configured
        self._send_webhook(notification)

    def _send_webhook(self, data: Dict[str, Any]):
        """Send data to webhook URL if available."""
        if not self.webhook_url:
            return

        try:
            headers = {"Content-Type": "application/json"}
            response = requests.post(
                self.webhook_url, headers=headers, data=json.dumps(data)
            )

            # Check response
            if response.status_code >= 400:
                print(f"Webhook error: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"Error sending webhook notification: {e}")

    def get_notification_log(self):
        """Get the notification log for debugging and monitoring."""
        return self.notification_log
