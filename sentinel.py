import time
import os
import re
import urllib.request
import json
from collections import Counter
import matplotlib.pyplot as plt

# Configuration
LOG_FILE = "server_logs.log"
KEYWORDS = ["FAILED", "ROOT", "SQL_INJECTION",
            "UNAUTHORIZED", "NMAP", "HONEYPOT"]


def get_location(ip):
    """Fetches the geographic location of an IP address."""
    # Skip local network IPs
    if ip.startswith("192.168.") or ip.startswith("10.") or ip.startswith("127."):
        return "Local Network (Your Home)"

    try:
        # Call a free Geo-IP API
        url = f"http://ip-api.com/json/{ip}"
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        if data['status'] == 'success':
            return f"{data['city']}, {data['country']}"
    except:
        pass
    return "Unknown Location"


def generate_dashboard():
    print("\n--- 📊 GENERATING BUSINESS THREAT REPORT ---")
    ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    attacker_ips = []

    with open(LOG_FILE, "r") as file:
        for line in file:
            for word in KEYWORDS:
                if word in line.upper():
                    ips_found = ip_pattern.findall(line)
                    attacker_ips.extend(ips_found)
                    break

    ip_counts = Counter(attacker_ips)
    if not ip_counts:
        print("[!] No attacks found to graph.")
        return

    ips = list(ip_counts.keys())
    counts = list(ip_counts.values())

    plt.figure(figsize=(10, 6))
    plt.bar(ips, counts, color='red')
    plt.title('Top Attacking IP Addresses (SOC Monitor)', fontsize=16)
    plt.xlabel('Hacker IP Address', fontsize=12)
    plt.ylabel('Number of Attack Attempts', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()

    print("[+] Dashboard generated! Close the graph window to exit.")
    plt.show()


def monitor_logs():
    print("--- 🛡️ PYTHON-SENTINEL SIEM ACTIVE ---")
    print(f"Monitoring {LOG_FILE} for suspicious activity...")
    print("Press Ctrl+C to stop monitoring and view the Threat Dashboard.\n")

    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, 'w').close()

    try:
        with open(LOG_FILE, "r") as file:
            file.seek(0, 2)

            while True:
                line = file.readline()
                if not line:
                    time.sleep(0.1)
                    continue

                for word in KEYWORDS:
                    if word in line.upper():
                        # Extract IP and look up location in real-time
                        ip_pattern = re.compile(
                            r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
                        ips_found = ip_pattern.findall(line)
                        location = get_location(
                            ips_found[0]) if ips_found else "Unknown"

                        print(
                            f"🚨 [ALERT] Threat from {location}: {line.strip()}")
                        break

    except KeyboardInterrupt:
        generate_dashboard()


if __name__ == "__main__":
    monitor_logs()
    
