from app_collector_local import SystemMonitor
from dotenv import load_dotenv, find_dotenv

# =================================================================================

# Loading environment variables
load_dotenv(find_dotenv(), override=True)

# =================================================================================

# Main function
def main():
    # Create an instance of the SystemMonitor class
    system_monitor = SystemMonitor()

    # Run the monitoring system
    system_monitor.run()


# =================================================================================

if __name__ == "__main__":
    main()
