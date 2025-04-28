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
        network_sent = network_io.bytes_sent / (1024 * 1024)  # Convert to MB
        network_received = network_io.bytes_recv / (1024 * 1024)  # Convert to MB
        print(f"Network Sent: {network_sent:.2f} MB")
        print(f"Network Received: {network_received:.2f} MB")

        # Get disk usage
        disk_usage_total = psutil.disk_usage('/').percent
        print(f"Total Disk Usage: {disk_usage_total}%")

        # Get disk read/write
        disk_io = psutil.disk_io_counters()
        disk_read = disk_io.read_bytes / (1024 * 1024)  # Convert to MB
        disk_write = disk_io.write_bytes / (1024 * 1024)  # Convert to MB
        print(f"Disk Read: {disk_read:.2f} MB")
        print(f"Disk Write: {disk_write:.2f} MB")

        # Get battery status
        battery = psutil.sensors_battery()
        if battery:
            battery_percentage = battery.percent
            battery_status = "Charging" if battery.power_plugged else "Not Charging"
            print(f"Battery Percentage: {battery_percentage}%")
            print(f"Battery Status: {battery_status}")
        else:
            print("Battery information not available.")

        # Get temperature (if available)
        try:
            temperature = psutil.sensors_temperatures()
            if temperature:
                for name, entries in temperature.items():
                    for entry in entries:
                        print(f"{name} - {entry.label or 'temp'}: {entry.current}°C")
            else:
                print("Temperature information not available.")
        except AttributeError:
            print("Temperature information not available.")

        print("=" * 10)

        time.sleep(5)
except KeyboardInterrupt:
    print("\nMonitoring stopped.")
except Exception as e:
    print(f"An error occurred: {e}")
