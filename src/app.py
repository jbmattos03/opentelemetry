"""
This script monitors the CPU and RAM usage of a system using OpenTelemetry and Prometheus.
It collects the metrics every 5 seconds and sends them to a Prometheus server.
It also prints the metrics to the console.

The script uses the psutil library to collect the CPU and RAM usage metrics.
The OpenTelemetry libraries are used to set up the monitoring system and collect the metrics.
The prometheus_client library is used to set up the Prometheus server and expose the metrics.
The program uses an OOP approach to organize the code and make it more modular.
"""

# =================================================================================

# Importing libraries
import time
from psutil import cpu_percent, virtual_memory, disk_usage, net_io_counters, disk_io_counters

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import start_http_server

# =================================================================================

class SystemMonitor:
    def __init__(self):
        self.set_exporters()
        self.set_meter()
        self.set_metrics()
        self.set_server()

    # =============== OpenTelemetry Setup ===============
    def set_exporters(self):
        """
        This method sets up the exporters.
        The console exporter is used to print the metrics to the console.
        """
        self.console_exporter = ConsoleMetricExporter()
    
    def set_readers(self):
        """
        This method sets up the readers.
        PeriodicExportingMetricReader is used to collect the metrics every 5 seconds.
        PrometheusMetricReader is used to expose the metrics to the Prometheus server.
        """
        self.prometheus_reader = PrometheusMetricReader()
        self.console_reader = PeriodicExportingMetricReader(self.console_exporter, export_interval_millis=5000)

    def set_meter(self):
        """
        This method sets up the meter.
        The meter is used to create and manage metrics.
        """
        self.meter = metrics.get_meter("system_monitor")

    def set_provider(self):
        """
        This method sets up the OpenTelemetry metrics provider.
        MeterProvider is used to manage the metrics.
        """
        self.provider = MeterProvider(metric_readers=[self.console_reader, self.prometheus_reader])
        metrics.set_meter_provider(self.provider)

    def set_metrics(self):
        """
        This method sets up the metrics.
        The CPU and RAM usage metrics are created as observable counters.
        """
        self.cpu_gauge = self.meter.create_observable_counter(
            "cpu_usage_total",
            callbacks=[self.cpu_callback],
            description="CPU usage percentage",
        )

        self.ram_gauge = self.meter.create_observable_counter(
            "ram_usage_total",
            callbacks=[self.ram_callback],
            description="RAM usage percentage",
        )

        self.disk_usage = self.meter.create_observable_counter(
            "disk_usage_total",
            callbacks=[self.disk_callback],
            description="Disk usage percentage",
        )

        self.disk_read = self.meter.create_observable_counter(
            "disk_read_total",
            callbacks=[self.disk_read_callback],
            description="Disk read in MB",
        )

        self.disk_write = self.meter.create_observable_counter(
            "disk_write_total",
            callbacks=[self.disk_write_callback],
            description="Disk write in MB",
        )

        self.network_sent = self.meter.create_observable_counter(
            "network_sent_total",
            callbacks=[self.network_sent_callback],
            description="Network sent in MB",
        )

        self.network_recv = self.meter.create_observable_counter(
            "network_recv_total",
            callbacks=[self.network_recv_callback],
            description="Network received in MB",
        )

    # Callback function for Total CPU usage metric
    def cpu_callback(self, options: metrics.CallbackOptions) -> list[metrics.Observation]:
        """
        This method is called every 5 seconds to collect the CPU usage metrics.
        It uses the psutil library to get the CPU usage percentage.
        The CPU usage percentage is returned as an observation.
        The observation is a list of metrics.Observation objects.
        """
        return [metrics.Observation(value=cpu_percent(interval=None), attributes={})]

    # Callback function for Total RAM Usage metric
    def ram_callback(self, options: metrics.CallbackOptions) -> list[metrics.Observation]:
        """
        This method is called every 5 seconds to collect the RAM usage metrics.
        It uses the psutil library to get the RAM usage percentage.
        The RAM usage percentage is returned as an observation.
        The observation is a list of metrics.Observation objects.
        """
        return [metrics.Observation(value=virtual_memory().percent, attributes={})]
    
    # Callback function for Total Disk Usage metric
    def disk_callback(self, options: metrics.CallbackOptions) -> list[metrics.Observation]:
        """
        This method is called every 5 seconds to collect the Disk usage metrics.
        It uses the psutil library to get the Disk usage percentage.
        The Disk usage percentage is returned as an observation.
        The observation is a list of metrics.Observation objects.
        """
        return [metrics.Observation(value=disk_usage("/").percent, attributes={})]
    
    # Callback function for Disk Read metric
    def disk_read_callback(self, options: metrics.CallbackOptions) -> list[metrics.Observation]:
        """
        This method is called every 5 seconds to collect the Disk read metrics.
        It uses the psutil library to get the Disk read in MB.
        The Disk read in MB is returned as an observation.
        The observation is a list of metrics.Observation objects.
        """
        return [metrics.Observation(value=round((disk_io_counters().read_bytes / (1024*1024)), 2), attributes={})]
    
    # Callback function for Disk Write metric
    def disk_write_callback(self, options: metrics.CallbackOptions) -> list[metrics.Observation]:
        """
        This method is called every 5 seconds to collect the Disk write metrics.
        It uses the psutil library to get the Disk write in MB.
        The Disk write in MB is returned as an observation.
        The observation is a list of metrics.Observation objects.
        """
        return [metrics.Observation(value=round((disk_io_counters().write_bytes / (1024*1024)), 2), attributes={})]
    
    # Callback functions for Network Sent metric
    def network_sent_callback(self, options: metrics.CallbackOptions) -> list[metrics.Observation]:
        """
        This method is called every 5 seconds to collect Network metrics (sent).
        It uses the psutil library to get the Network sent in MB.
        The Network sent in MB is returned as an observation.
        The observation is a list of metrics.Observation objects.
        """
        return [metrics.Observation(value=round((net_io_counters().bytes_sent / (1024*1024)), 2), attributes={})]
    
    # Callback function for Network Received metric
    def network_recv_callback(self, options: metrics.CallbackOptions) -> list[metrics.Observation]:
        """
        This method is called every 5 seconds to collect Network metrics (received).
        It uses the psutil library to get the Network sent in MB.
        The Network sent in MB is returned as an observation.
        The observation is a list of metrics.Observation objects.
        """
        return [metrics.Observation(value=round((net_io_counters().bytes_recv / (1024*1024)), 2), attributes={})]
    
    # =============== Prometheus Setup ===============
    def set_server(self):
        """
        This method sets up the Prometheus server.
        The server is started on port 8001.
        The metrics are exposed at the /metrics endpoint.
        """
        try:
            start_http_server(8001)
            print("Prometheus server started at http://localhost:8001")
        except Exception as e:
            print(f"Error starting Prometheus server: {e}")

    # =============== Run Function ===============
    def run(self):
        """
        This method will stall for 5 seconds to let PeriodicExportingMetricReader()
        collect the metrics.
        It will also print the metrics to the console.
        """
        print("Starting system monitoring...")

        try:
            self.set_readers()
            self.set_provider()

            self.running = True

            while self.running:
                # Keep the program alive, waiting for metrics to be collected
                time.sleep(5)
        except KeyboardInterrupt:
            self.running = False

            print("Monitoring stopped.")
        except Exception as e:
            print(f"An error occurred: {e}")

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
