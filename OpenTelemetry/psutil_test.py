import psutil
import time

try:
    while True:
        # Get CPU usage
        cpu_usage = psutil.cpu_percent(interval=None)
        print(f"CPU Usage: {cpu_usage}%")

        # Get RAM usage
        ram_usage = psutil.virtual_memory().percent
        print(f"RAM Usage: {ram_usage}%")

        time.sleep(5)
except KeyboardInterrupt:
    print("\nMonitoring stopped.")
except Exception as e:
    print(f"An error occurred: {e}")
