import sys
import dotenv
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
dotenv.load_dotenv()

from app_collector_local import SystemMonitor
import timeit

# Define the function to be benchmarked
def benchmark_system_monitor():
    monitor = SystemMonitor()

    cpu = timeit.timeit(lambda: monitor.cpu_callback(None), number=20000)
    if cpu:
        print("CPU")
    ram = timeit.timeit(lambda: monitor.ram_callback(None), number=20000)
    if ram:
        print("RAM")
    disk_read = timeit.timeit(lambda: monitor.disk_read_callback(None), number=20000)
    if disk_read:
        print("disk_read")
    disk_write = timeit.timeit(lambda: monitor.disk_write_callback(None), number=20000)
    if disk_write:
        print("disk_write")
    network_recv = timeit.timeit(lambda: monitor.network_recv_callback(None), number=20000)
    if network_recv:
        print("network_recv")
    network_sent = timeit.timeit(lambda: monitor.network_sent_callback(None), number=20000)
    if network_sent:
        print("network_sent")

    return {"cpu": cpu, 
            "ram": ram, 
            "disk_read": disk_read, 
            "disk_write": disk_write, 
            "network_recv": network_recv, 
            "network_sent": network_sent}

# Run the benchmark
if __name__ == "__main__":
    benchmark_results = benchmark_system_monitor()
    print("Benchmark Results:")
    for key, value in benchmark_results.items():
        print(f"{key}: {value:.6f} seconds")