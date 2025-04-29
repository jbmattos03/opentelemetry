"""
This module is used to manage alerts.
It allows you to set, delete, and check alerts based on system metrics.
It also allows you to dump the alerts to a JSON file.
The alerts are used to notify the user when a certain condition is met.
"""

import os, json, datetime

class AlertManager:
    def __init__(self, device_type):
        self.device_type = device_type
        self.set_alerts(device_type)

    def add_alert(self, alert_name, threshold, message):
        """
        This method adds a new alert.
        """
        if self.device_type == "Mobile":
            self.alerts[alert_name] = {
                "threshold": threshold[0],
                "message": message,
            }
        elif self.device_type == "Desktop":
            self.alerts[alert_name] = {
                "threshold": threshold[1],
                "message": message,
            }
        else:
            self.alerts[alert_name] = {
                "threshold": threshold[2],
                "message": message,
            }

    def set_alerts(self, device_type):
        """
        This method sets up the alerts.
        The thresholds are set based on the device type.
        The default thresholds are set for Android, Linux, Windows, and MacOS.
        """
        default_thresholds = {
            "cpu_usage": 50,
            "memory_usage": 50,
            "disk_usage": 50,
            "disk_read": 100000000,
            "disk_write": 100000000,
            "network_sent": 50000000,
            "network_recv": 50000000,
        }

        device_specific_thresholds = {
            "Android": {
                "cpu_usage": 40,
                "memory_usage": 30,
                "disk_usage": 90,
                "disk_read": 100000000,
                "disk_write": 100000000,
                "network_sent": 10000000,
                "network_recv": 10000000,
            },
            "Linux": {
                "cpu_usage": 50,
                "memory_usage": 60,
                "disk_usage": 80,
                "disk_read": 400000000,
                "disk_write": 400000000,
                "network_sent": 10000000,
                "network_recv": 10000000,
            },
            "Windows": {
                "cpu_usage": 50,
                "memory_usage": 60,
                "disk_usage": 80,
                "disk_read": 400000000,
                "disk_write": 400000000,
                "network_sent": 10000000,
                "network_recv": 10000000,
            },
            "MacOS": {
                "cpu_usage": 50,
                "memory_usage": 60,
                "disk_usage": 80,
                "disk_read": 400000000,
                "disk_write": 400000000,
                "network_sent": 10000000,
                "network_recv": 10000000,
            },
        }

        thresholds = device_specific_thresholds.get(device_type, default_thresholds)

        self.alerts = {
            metric: {
                "threshold": thresholds.get(metric, default_thresholds[metric]),
                "message": f"{metric.replace('_', ' ').capitalize()} is above {thresholds.get(metric, default_thresholds[metric])}",
            }
            for metric in default_thresholds
        }

    def delete_alerts(self, alerts):
        """
        This method deletes the alerts.
        """
        for alert in alerts:
            if alert in self.alerts:
                del self.alerts[alert]
            else:
                print(f"Alert {alert} not found.")

    def dump_alerts(self, alert_event):
        """
        This method dumps the alerts to a JSON file.
        """
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


    def check_alerts(self, alert, value, host):
        """
        This method checks the alerts.
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

            # Dump the alert event to a JSON file
            self.dump_alerts(alert_event)
