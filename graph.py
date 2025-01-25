import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load data from CSV
data = pd.read_csv("elasticsearch_metrics.csv")

# Convert timestamp from UNIX to readable datetime if necessary
try:
    # Attempt to convert assuming UNIX timestamps
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s')
except ValueError:
    # If already in readable format
    data['timestamp'] = pd.to_datetime(data['timestamp'], format='%d-%m-%Y %H:%M')

# Ensure all columns are properly converted
timestamps = data['timestamp']
cpu_percent = data['cpu_percent'].astype(float)
memory_percent = data['memory_percent'].astype(float)
load_avg = data['load_avg'].astype(float)

# Calculate averages
cpu_avg = cpu_percent.mean()
memory_avg = memory_percent.mean()
load_avg_mean = load_avg.mean()

# Print averages to console
print(f"Average CPU Usage: {cpu_avg:.2f}%")
print(f"Average Memory Usage: {memory_avg:.2f}%")
print(f"Average Load Average: {load_avg_mean:.2f}")

# Create a figure with two subplots
fig, ax = plt.subplots(2, 1, figsize=(12, 8))

# Plot CPU usage
ax[0].plot(timestamps, cpu_percent, label="CPU Usage (%)", color="green")
ax[0].axhline(cpu_avg, color="red", linestyle="--", label=f"Average CPU Usage: {cpu_avg:.2f}%")
ax[0].set_title("CPU Usage Over Time")
ax[0].set_ylabel("CPU Usage (%)")
ax[0].set_xlabel("Time")
ax[0].legend(loc="upper right")
ax[0].grid(True)

# Plot memory usage and load average
ax[1].plot(timestamps, memory_percent, label="Memory Usage (%)", color="blue")
ax[1].axhline(memory_avg, color="red", linestyle="--", label=f"Average Memory Usage: {memory_avg:.2f}%")
ax[1].plot(timestamps, load_avg, label="Load Average", color="orange")
ax[1].axhline(load_avg_mean, color="purple", linestyle="--", label=f"Average Load Average: {load_avg_mean:.2f}")
ax[1].set_title("Memory Usage and Load Average")
ax[1].set_ylabel("Percentage / Load")
ax[1].set_xlabel("Time")
ax[1].legend(loc="upper right")
ax[1].grid(True)

# Adjust layout
plt.tight_layout()

# Save the plot as a JPEG file
output_file = "metrics_graph_with_averages.jpeg"
plt.savefig(output_file, format="jpeg")
print(f"Graph saved as {output_file}")
