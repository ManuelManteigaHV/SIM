import random
import time
from datetime import datetime

# Define log format templates
log_formats = {
    "firewall": "{timestamp} | FIREWALL | Source IP: {src_ip} | Destination IP: {dst_ip} | Action: {action}",
    "ids": "{timestamp} | IDS | Alert: {alert} | Source IP: {src_ip} | Destination IP: {dst_ip} | Severity: {severity}",
    "application": "{timestamp} | APP | User: {user} | Action: {action} | Status: {status}"
}

# Sample data for logs
actions = ["ALLOW", "DENY", "DROP"]
alerts = ["Port Scan Detected", "SQL Injection", "Malware Detected"]
users = ["alice", "bob", "charlie", "admin"]
statuses = ["SUCCESS", "FAILURE"]
severities = ["LOW", "MEDIUM", "HIGH"]

# Generate random IP address
def random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

# Generate a random log line
def generate_log(log_type):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if log_type == "firewall":
        return log_formats[log_type].format(
            timestamp=timestamp,
            src_ip=random_ip(),
            dst_ip=random_ip(),
            action=random.choice(actions)
        )
    elif log_type == "ids":
        return log_formats[log_type].format(
            timestamp=timestamp,
            alert=random.choice(alerts),
            src_ip=random_ip(),
            dst_ip=random_ip(),
            severity=random.choice(severities)
        )
    elif log_type == "application":
        return log_formats[log_type].format(
            timestamp=timestamp,
            user=random.choice(users),
            action=random.choice(["login", "logout", "update", "delete"]),
            status=random.choice(statuses)
        )
    else:
        return "Unknown log type."

# Simulate logs for a specific type
def simulate_logs_random(count=10, delay=1):
    log_types = list(log_formats.keys())
    print(f"Generating {count} random logs...")
    for _ in range(count):
        log_type = random.choice(log_types)
        print(generate_log(log_type))
        time.sleep(delay)

# Example usage
if __name__ == "__main__":
    count = int(input("Enter number of logs to generate: "))
    simulate_logs_random(count)

