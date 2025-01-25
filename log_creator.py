import random
import time
import json
from datetime import datetime

log_formats = {
    "firewall": {
        "index": {"_index": "firewall-logs"},
        "log": {
            "timestamp": "{timestamp}",
            "category": "FIREWALL",
            "source_ip": "{src_ip}",
            "destination_ip": "{dst_ip}",
            "action": "{action}"
        }
    },
    "ids": {
        "index": {"_index": "ids-logs"},
        "log": {
            "timestamp": "{timestamp}",
            "category": "IDS",
            "alert": "{alert}",
            "source_ip": "{src_ip}",
            "destination_ip": "{dst_ip}",
            "severity": "{severity}"
        }
    },
    "application": {
        "index": {"_index": "application-logs"},
        "log": {
            "timestamp": "{timestamp}",
            "category": "APP",
            "user": "{user}",
            "action": "{action}",
            "status": "{status}"
        }
    }
}

actions = ["ALLOW", "DENY", "DROP"]
alerts = ["Port Scan Detected", "SQL Injection", "Malware Detected"]
users = ["alice", "bob", "charlie", "admin"]
statuses = ["SUCCESS", "FAILURE"]
severities = ["LOW", "MEDIUM", "HIGH"]

def random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

def generate_log(log_type):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if log_type == "firewall":
        return {
            "index": log_formats[log_type]["index"],
            "log": {
                "timestamp": timestamp,
                "category": "FIREWALL",
                "source_ip": random_ip(),
                "destination_ip": random_ip(),
                "action": random.choice(actions)
            }
        }
    elif log_type == "ids":
        return {
            "index": log_formats[log_type]["index"],
            "log": {
                "timestamp": timestamp,
                "category": "IDS",
                "alert": random.choice(alerts),
                "source_ip": random_ip(),
                "destination_ip": random_ip(),
                "severity": random.choice(severities)
            }
        }
    elif log_type == "application":
        return {
            "index": log_formats[log_type]["index"],
            "log": {
                "timestamp": timestamp,
                "category": "APP",
                "user": random.choice(users),
                "action": random.choice(["login", "logout", "update", "delete"]),
                "status": random.choice(statuses)
            }
        }
    else:
        return None

def simulate_logs_to_json(file_name, count=10, delay=1):
    log_types = list(log_formats.keys())
    
    with open(file_name, "w") as file:
        for _ in range(count):
            log_type = random.choice(log_types)
            log_entry = generate_log(log_type)
            if log_entry:
                file.write(json.dumps(log_entry["index"]) + "\n")
                file.write(json.dumps(log_entry["log"]) + "\n")
            time.sleep(delay)

if __name__ == "__main__":
    count = int(input("Enter number of logs to generate: "))
    file_name = f"logs_{count}.json"
    print(f"Generating {count} logs into {file_name}...")
    simulate_logs_to_json(file_name, count)
    print(f"Logs written to {file_name}")
