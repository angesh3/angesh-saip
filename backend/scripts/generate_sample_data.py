import requests
import random
from datetime import datetime, timedelta
import time
import os

# Sample data
users = ["user1", "user2", "user3", "user4", "user5"]
resources = ["database", "api", "admin_panel", "file_server", "vpn"]
actions = ["read", "write", "execute", "connect", "login"]
locations = ["US", "UK", "DE", "FR", "JP"]
device_types = ["desktop", "laptop", "mobile", "tablet"]

def generate_access_log():
    return {
        "user_id": random.choice(users),
        "timestamp": (datetime.now() - timedelta(minutes=random.randint(0, 60))).isoformat(),
        "resource": random.choice(resources),
        "action": random.choice(actions),
        "ip_address": f"192.168.1.{random.randint(1, 255)}",
        "location": random.choice(locations),
        "device_type": random.choice(device_types),
        "status": "success"
    }

def generate_anomaly_log():
    # Generate an anomalous log (e.g., unusual time, location, or multiple failed attempts)
    log = generate_access_log()
    if random.random() < 0.5:
        # Unusual time (outside normal hours)
        log["timestamp"] = (datetime.now() - timedelta(hours=random.randint(2, 5))).isoformat()
    else:
        # Failed attempt
        log["status"] = "failed"
    return log

def main():
    # Use the service name from docker-compose as the hostname
    base_url = "http://backend:8000"
    
    print(f"Generating sample data and sending to {base_url}")
    
    # Generate normal logs
    for _ in range(20):
        log = generate_access_log()
        try:
            response = requests.post(f"{base_url}/logs/", json=log)
            print(f"Posted normal log: {response.status_code}")
        except Exception as e:
            print(f"Error posting log: {e}")
        time.sleep(1)
    
    # Generate some anomalies
    for _ in range(5):
        log = generate_anomaly_log()
        try:
            response = requests.post(f"{base_url}/logs/", json=log)
            print(f"Posted anomaly log: {response.status_code}")
        except Exception as e:
            print(f"Error posting log: {e}")
        time.sleep(1)
    
    print("Sample data generation complete!")

if __name__ == "__main__":
    main() 