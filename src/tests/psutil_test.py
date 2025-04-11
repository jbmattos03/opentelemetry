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

        # Get network usage
        network_io = psutil.net_io_counters()
        network_sent = network_io.bytes_sent
        network_received = network_io.bytes_recv
        print(f"Network Sent: {network_sent} bytes")
        print(f"Network Received: {network_received} bytes")

        # Get disk usage
        disk_usage_total = psutil.disk_usage('/').percent
        print(f"Total Disk Usage: {disk_usage_total}%")

        print("=" * 10)

        time.sleep(5)
except KeyboardInterrupt:
    print("\nMonitoring stopped.")
except Exception as e:
    print(f"An error occurred: {e}")
