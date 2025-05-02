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
    disk = timeit.timeit(lambda: monitor.disk_callback(None), number=20000)
    if disk:
        print("disk")
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
            "disk": disk,
            "disk_read": disk_read,
            "disk_write": disk_write, 
            "network_recv": network_recv, 
            "network_sent": network_sent}

# Calculate mean and std dev for each metric
def stats(n):
    benchmark_results = []

    for _ in range(n):
        print(f"Iteration {i}")
        benchmark_results.append(benchmark_system_monitor())
    
    # Calculating the mean for each metric
    mean = {}
    std_dev = {} 
    for metric in benchmark_results[0].keys():
        mean[metric] = sum(result[metric] for result in benchmark_results) / len(benchmark_results)
        std_dev[metric] = (sum((result[metric] - mean[metric]) ** 2 for result in benchmark_results) / len(benchmark_results)) ** 0.5
    
    return mean, std_dev


# Run the benchmark
if __name__ == "__main__":
    benchmark_results = benchmark_system_monitor()
    print("Benchmark Results:")
    for key, value in benchmark_results.items():
        print(f"{key}: {value:.6f} seconds")
    
    mean, std_dev = stats(10)
    print("\nMean and Standard Deviation of Benchmark Results:")
    for m, s in zip(mean.keys(), std_dev.keys()):
        print(f"{m}: {mean[m]:.6f} \u00B1 {std_dev[s]:.6f} seconds")
    
