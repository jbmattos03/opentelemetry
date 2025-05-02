# =================================================================================

# Importing libraries
import cython
import time
import os
import sys
from dotenv import load_dotenv, find_dotenv
from alert_manager import AlertManager

from psutil import cpu_percent, virtual_memory, disk_usage, net_io_counters, disk_io_counters
from opentelemetry import metrics
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter

# =================================================================================

# Loading environment variables
load_dotenv(find_dotenv(), override=True)

# =================================================================================

cdef class SystemMonitor:
    cdef object resource
    cdef object collector_exporter
    cdef object collector_reader
    cdef object meter
    cdef object provider
    cdef object cpu_gauge
    cdef object ram_gauge
    cdef object disk_usage
    cdef object disk_read
    cdef object disk_write
    cdef object network_sent
    cdef object network_recv
    cdef object alert_manager
    cdef str device_type
    cdef bint running

    def __init__(self):
        self.set_exporters()
        self.set_meter()
        self.set_metrics()
        self.set_resource()
        self.device_type = self.detect_device_type()
        self.alert_manager = AlertManager(self.device_type)

    # =============== OpenTelemetry Setup ===============
    def set_resource(self):
        """
        This method sets up the resource.
        The resource is used to identify the source of the metrics.
        """
        self.resource = Resource.create({SERVICE_NAME: f"{os.getenv('HOST')}_system_monitor"})

    def set_exporters(self):
        """
        This method sets up the exporters.
        The OTLP Collector is used to collect the data, then expose and send them to Prometheus.
        """
        self.collector_exporter = OTLPMetricExporter(endpoint=f"http://{os.getenv('IP_ADDR')}:4318/v1/metrics")

    def set_readers(self):
        """
        This method sets up the readers.
        PeriodicExportingMetricReader is used to collect the metrics every 5 seconds.
        """
        self.collector_reader = PeriodicExportingMetricReader(self.collector_exporter, export_interval_millis=5000)

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
        self.provider = MeterProvider(metric_readers=[self.collector_reader], resource=self.resource)
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
            description="Disk read in bytes",
        )

        self.disk_write = self.meter.create_observable_counter(
            "disk_write_total",
            callbacks=[self.disk_write_callback],
            description="Disk write in bytes",
        )

        self.network_sent = self.meter.create_observable_counter(
            "network_sent_total",
            callbacks=[self.network_sent_callback],
            description="Network sent in bytes",
        )

        self.network_recv = self.meter.create_observable_counter(
            "network_recv_total",
            callbacks=[self.network_recv_callback],
            description="Network received in bytes",
        )

    # Callback function for Total CPU usage metric
    cpdef cpu_callback(self, object options):
        """
        This method is called every 5 seconds to collect the CPU usage metrics.
        It uses the psutil library to get the CPU usage percentage.
        The CPU usage percentage is returned as an observation.
        The observation is a list of metrics.Observation objects.
        It also checks for alerts using the AlertManager class.
        """
        cdef double cpu_usage

        cpu_usage = cpu_percent(interval=None)
        self.alert_manager.check_alerts("cpu_usage", cpu_usage, os.getenv("HOST"))

        return [metrics.Observation(value=cpu_usage, attributes={})]
    
    # Callback function for Total RAM Usage metric
    cpdef ram_callback(self, object options):
        """
        This method is called every 5 seconds to collect the RAM usage metrics.
        It uses the psutil library to get the RAM usage percentage.
        The RAM usage percentage is returned as an observation.
        The observation is a list of metrics.Observation objects.
        It also checks for alerts using the AlertManager class.
        """
        cdef double ram_usage

        ram_usage = virtual_memory().percent
        self.alert_manager.check_alerts("memory_usage", ram_usage, os.getenv("HOST"))

        return [metrics.Observation(value=ram_usage, attributes={})]
    
    # Callback function for Total Disk Usage metric
    cpdef disk_callback(self, object options):
        """
        This method is called every 5 seconds to collect the Disk usage metrics.
        It uses the psutil library to get the Disk busy time in milliseconds
        during 4 seconds, then divides it by 4000 to get the percentage.
        The Disk busy time percentage is returned as an observation.
        The observation is a list of metrics.Observation objects.
        It also checks for alerts using the AlertManager class.
        """
        cdef double disk_total
        disk_total = disk_io_counters().busy_time / 1000

        self.alert_manager.check_alerts("disk_total", disk_total, os.getenv("HOST"))

        return [metrics.Observation(value=disk_total, attributes={})]
    
    # Callback function for Disk Read metric
    cpdef disk_read_callback(self, object options):
        """
        This method is called every 5 seconds to collect the Disk read metrics.
        It uses the psutil library to get the Disk read in bytes.
        The Disk read in bytes is returned as an observation.
        The observation is a list of metrics.Observation objects.
        It also checks for alerts using the AlertManager class.
        """
        cdef long long int disk_read
        
        disk_read = disk_io_counters().read_bytes
        self.alert_manager.check_alerts("disk_read", disk_read, os.getenv("HOST"))

        return [metrics.Observation(value=disk_read, attributes={})]
    
    # Callback function for Disk Write metric
    cpdef disk_write_callback(self, object options):
        """
        This method is called every 5 seconds to collect the Disk write metrics.
        It uses the psutil library to get the Disk write in bytes.
        The Disk write in bytes is returned as an observation.
        The observation is a list of metrics.Observation objects.
        It also checks for alerts using the AlertManager class.
        """
        cdef long long int disk_write

        disk_write = disk_io_counters().write_bytes
        self.alert_manager.check_alerts("disk_write", disk_write, os.getenv("HOST"))

        return [metrics.Observation(value=disk_write, attributes={})]
    
    # Callback functions for Network Sent metric
    cpdef network_sent_callback(self, object options):
        """
        This method is called every 5 seconds to collect Network metrics (sent).
        It uses the psutil library to get the Network sent in bytes.
        The Network sent in bytes is returned as an observation.
        The observation is a list of metrics.Observation objects.
        It also checks for alerts using the AlertManager class.
        """
        cdef long long int net_sent

        net_sent = net_io_counters().bytes_sent
        self.alert_manager.check_alerts("network_sent", net_sent, os.getenv("HOST"))

        return [metrics.Observation(value=net_sent, attributes={})]
    
    # Callback function for Network Received metric
    cpdef list network_recv_callback(self, object options):
        """
        This method is called every 5 seconds to collect Network metrics (received).
        It uses the psutil library to get the Network sent in bytes.
        The Network sent in bytes is returned as an observation.
        The observation is a list of metrics.Observation objects.
        It also checks for alerts using the AlertManager class.
        """
        cdef long long int net_recv

        net_recv = net_io_counters().bytes_recv
        self.alert_manager.check_alerts("network_recv", net_recv, os.getenv("HOST"))

        return [metrics.Observation(value=net_recv, attributes={})]

    # =============== Run Function ===============
    def run(self):
        """
        This method will stall for 5 seconds to let PeriodicExportingMetricReader() collect the metrics.
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

    # =============== Detect Device Function ===============
    def detect_device_type(self):
        """
        Detects the type of device based on the system information.
        """
        try:
            if hasattr(sys, 'getandroidapilevel'):
                return "Android"
            elif sys.platform.startswith("linux"):
                return "Linux"
            elif sys.platform.startswith("darwin"):
                return "MacOS"
            elif sys.platform.startswith("win"):
                return "Windows"
            else:
                return str("Unknown")
        except AttributeError as e:
            print(f"Error detecting device type: {e}")
            return "Unknown"
            