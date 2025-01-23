import psutil
import time
import csv
from datetime import datetime

# Define file to log metrics
LOG_FILE = "elasticsearch_metrics.csv"

# Write headers to the CSV file
with open(LOG_FILE, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["timestamp", "cpu_percent", "memory_percent", "load_avg"])

def get_elasticsearch_metrics():
    """Get metrics specifically for Elasticsearch processes."""
    cpu_usage = 0.0
    mem_usage = 0.0

    # Iterate through all running processes
    for proc in psutil.process_iter(attrs=["name", "cpu_percent", "memory_percent"]):
        try:
            # Check if the process name matches Elasticsearch (typically "java" or "elastic")
            if "java" in proc.info["name"].lower() or "elastic" in proc.info["name"].lower():
                cpu_usage += proc.info["cpu_percent"]
                mem_usage += proc.info["memory_percent"]
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return cpu_usage, mem_usage

print("Monitoring Elasticsearch metrics... Press Ctrl+C to stop.")

try:
    while True:
        cpu_usage, mem_usage = get_elasticsearch_metrics()

        load_avg = psutil.getloadavg()[0]  # 1-minute load average

        # Convert timestamp to readable format
        readable_timestamp = datetime.now().strftime("%d-%m-%Y %H:%M")

        metrics = {
            "timestamp": readable_timestamp,
            "cpu_percent": cpu_usage,
            "memory_percent": mem_usage,
            "load_avg": load_avg,
        }
        print("timestamp: {}, cpu_percent: {:.2f}, memory_percent: {:.2f}, load_avg: {:.2f}".format(
            metrics['timestamp'], metrics['cpu_percent'], metrics['memory_percent'], metrics['load_avg']
        ))

        # Write metrics to CSV
        with open(LOG_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(metrics.values())

        # Monitor every second
        time.sleep(1)

except KeyboardInterrupt:
    print("Metrics logged to {}".format(LOG_FILE))
