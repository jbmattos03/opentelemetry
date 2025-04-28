"""
This module is used to manage alerts.
It allows you to set, delete, and check alerts based on system metrics.
It also allows you to dump the alerts to a JSON file.
The alerts are used to notify the user when a certain condition is met.
"""

import os, json, datetime

class AlertManager:
    def __init__(self):
        self.set_alerts()

    def add_alert(self, alert_name, threshold, message):
        """
        This method adds a new alert.
        The alert is used to notify the user when a certain condition is met.
        """
        self.alerts[alert_name] = {
            "threshold": threshold,
            "message": message,
        }

    def set_alerts(self):
        """
        This method sets up the alerts.
        The alerts are used to notify the user when a certain condition is met.
        """
        self.alerts = {
            "cpu_usage": {
                "threshold": 50,
                "message": "CPU usage is above 50%",
            },
            "memory_usage": {
                "threshold": 60,
                "message": "Memory usage is above 60%",
            },
            "disk_usage": {
                "threshold": 80,
                "message": "Disk usage is above 80%",
            },
            "disk_read": {
                "threshold": 100000000,
                "message": "Disk read is above 100MB",
            },
            "disk_write": {
                "threshold": 100000000,
                "message": "Disk write is above 100MB",
            },
            "network_sent": {
                "threshold": 50000000,
                "message": "Network sent is above 50MB",
            },
            "network_recv": {
                "threshold": 50000000,
                "message": "Network received is above 50MB",
            },
        }

    def delete_alerts(self, alerts):
        """
        This method deletes the alerts.
        The alerts are used to notify the user when a certain condition is met.
        """
        for alert in alerts:
            if alert in self.alerts:
                del self.alerts[alert]
            else:
                print(f"Alert {alert} not found.")

    def check_alerts(self, alert, value, host):
        """
        This method checks the alerts.
        The alerts are used to notify the user when a certain condition is met.
        """
        if alert in self.alerts and value >= self.alerts[alert]["threshold"]:
            # Add a time stamp for the alert
            alert_event = {
                "alert": alert,
                "host": host,
                "value": value,
                "threshold": self.alerts[alert]["threshold"],
                "message": self.alerts[alert]["message"],
                "timestamp": datetime.datetime.now().strftime('%H:%M:%S')
            }

            # Load existing alerts from the JSON file
            alerts_list = []
            if os.path.exists("alerts.json"):
                with open("alerts.json", "r") as f:
                    try:
                        alerts_list = json.load(f)
                    except Exception as e:
                        print(f"Error loading alerts: {e}")
                        alerts_list = []
            
            # Append the new alert event to the list
            alerts_list.append(alert_event)

            # Write the updated alerts list back to the JSON file
            with open("alerts.json", "w") as f:
                json.dump(alerts_list, f, indent=4)
