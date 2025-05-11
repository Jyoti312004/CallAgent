import requests
import json
import os
from typing import Optional, Dict, Any
from datetime import datetime
import logging
logger = logging.getLogger("app_logger")

class Notifier:
    """Handles notifications to supervisors and customers."""

    def __init__(self, webhook_url=None):
        """Initialize with optional webhook URL."""
        self.webhook_url = webhook_url or os.environ.get("NOTIFICATION_WEBHOOK_URL")
        logger.info(f"Webhook URL: {self.webhook_url}")
        self.notification_log = []

    def notify_supervisor(self, request_id: str, message: str):
        """Notify a supervisor about a help request."""
        notification = {
            "type": "supervisor_notification",
            "request_id": request_id,
            "message": message,
            "timestamp": datetime.now().isoformat(),
        }

        self.notification_log.append(notification)

        logger.info(f"\n[SUPERVISOR NOTIFICATION] Request ID: {request_id}")
        logger.info(f"Message: {message}")

        self._send_webhook(notification)

    def notify_customer(self, customer_id: str, email: str,message: str,question:str=''):
        """Notify a customer with a response."""
        notification = {
            "type": "customer_notification",
            "customer_id": customer_id,
            "email": email,
            "question": question,
            "message": message,
            "timestamp": datetime.now().isoformat(),
        }

        self.notification_log.append(notification)

        logger.info(f"\n[CUSTOMER NOTIFICATION] Customer ID: {customer_id}")
        logger.info(f"Message: {message}")
        
        self._send_webhook(notification)

    def _send_webhook(self, data: Dict[str, Any]):
        """Send data to webhook URL if available."""
        if not self.webhook_url:
            return

        try:
            logger.info(f"Sending webhook to {self.webhook_url} with data: {data}")
            headers = {"Content-Type": "application/json"}
            response = requests.post(
                self.webhook_url, headers=headers, json=data
            )

            if response.status_code >= 400:
                logger.info(f"Webhook error: {response.status_code} - {response.text}")

            logger.info("Webhook sent successfully. Response:", response.status_code)
        except Exception as e:
            logger.error(f"Error sending webhook notification: {e}")

    def get_notification_log(self):
        """Get the notification log for debugging and monitoring."""
        return self.notification_log
