# 🛡️ Python Sentinel: Custom SIEM & Honeypot

## 📖 Overview
Python Sentinel is a custom-built, lightweight Security Information and Event Management (SIEM) tool and Network Honeypot written entirely in Python. It was engineered to monitor server logs in real-time, detect malicious network activity using Regular Expressions, and trap attackers using a live network socket honeypot.

This project demonstrates core SOC (Security Operations Center) capabilities, transitioning raw log data into actionable Threat Intelligence.

## ✨ Key Features
* **Live Threat Monitoring:** Utilizes Python File I/O to continuously monitor server logs in real-time without locking the file system.
* **Network Honeypot Trap:** Opens a vulnerable mock port (e.g., Port 2222) via the `socket` library to bait attackers. Intercepts incoming connections, logs the attacker's IP address, and safely drops the connection.
* **Geographic Threat Intelligence:** Integrates with a Geo-IP API using `urllib` and `json` to automatically resolve attacker IP addresses to their physical City and Country in real-time.
* **Signature-Based Detection:** Employs `re` (Regular Expressions) to parse logs for specific threat signatures like `SQL_INJECTION`, `NMAP` scans, and brute-force `FAILED` logins.
* **Automated SOC Dashboard:** Uses `matplotlib` to automatically aggregate attack data and generate a visual bar chart of the top attacking IP addresses upon system exit.

## 🛠️ Technologies Used
* **Language:** Python 3
* **Libraries:** `socket`, `re`, `json`, `urllib`, `collections`, `time`, `os`, `matplotlib`
* **Testing Environment:** Kali Linux (Attacker VM), Netcat (`nc`), Windows Host

## 🚀 How It Works
1. The `honeypot.py` script binds to `0.0.0.0` and listens for unauthorized access attempts.
2. When an attacker (e.g., from a Kali Linux VM) attempts a connection, the Honeypot logs their IP as a severe threat.
3. The `sentinel.py` SIEM script reads this log in real-time, extracts the IP, looks up the geographic location, and alerts the SOC analyst.
4. Upon termination, the SIEM generates an Incident Response visual dashboard showing attack frequencies.
5.
