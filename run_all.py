import subprocess
import time
import os
import signal

monitor_script = "monitoring.py"  
graph_script = "graph2.py" 

try:
    # Ask the user for the log file name
    log_file = input("Enter the log file name (e.g., logs_10000.txt): ").strip()

    if not os.path.isfile(log_file):
        print(f"Error: File '{log_file}' not found. Please ensure the file exists.")
        exit(1)

    curl_command = [
        "curl", "-X", "POST",
        "http://localhost:9200/_bulk",
        "-H", "Content-Type: application/json",
        "--data-binary", f"@{log_file}"
    ]

    # Start the monitor script using python3
    print("Starting monitor script...")
    monitor_process = subprocess.Popen(["python3", monitor_script])  # Start monitor in the background
    print(f"Monitor script started with PID {monitor_process.pid}.")

    # Wait for 10 seconds before running the curl command
    print("Waiting for 10 seconds before running the curl command...")
    time.sleep(10)

    # Run the curl command
    print("Running curl command...")
    subprocess.run(curl_command, check=True)
    print("Curl command executed successfully.")

    # Wait for the remaining time to complete 1 minute since the monitor started
    remaining_time = 50  # 60 seconds total minus the 10 seconds already waited
    print(f"Waiting for {remaining_time} seconds to complete 1 minute...")
    time.sleep(remaining_time)

    # Stop the monitor script
    print("Stopping monitor script...")
    monitor_process.terminate() 
    try:
        monitor_process.wait(timeout=5)  # Wait up to 5 seconds for the process to terminate
        print("Monitor script terminated successfully.")
    except subprocess.TimeoutExpired:
        print("Monitor script did not terminate, killing it forcefully...")
        monitor_process.kill()  # Forcefully kill the process
        print("Monitor script killed.")

    # Run the graph generation script using python3
    print("Running graph generation script...")
    subprocess.run(["python3", graph_script], check=True)
    print("Graph generation script executed successfully.")

except subprocess.CalledProcessError as e:
    print(f"An error occurred while executing a command: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
