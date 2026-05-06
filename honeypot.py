import socket
import time

# Configuration
PORT = 2222  # A fake port we are opening to trap hackers
LOG_FILE = "server_logs.log"


def start_honeypot():
    print(f"--- 🍯 HONEYPOT ACTIVE ---")
    print(f"[+] Listening for attacks on port {PORT}...")

    # Set up the network socket to listen on all IP addresses (0.0.0.0)
    trap = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    trap.bind(("0.0.0.0", PORT))
    trap.listen(5)

    while True:
        try:
            # Wait for a hacker to connect
            conn, addr = trap.accept()
            attacker_ip = addr[0]

            print(f"🚨 [BINGO] Incoming attack from {attacker_ip}!")

            # Write the attack to our log file so Sentinel can catch it
            with open(LOG_FILE, "a") as f:
                f.write(
                    f"{attacker_ip} - FAILED login attempt for user 'root' (HONEYPOT TRAP)\n")

            # Send a fake server message to trick the hacker, then drop them
            conn.send(b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1\r\n")
            time.sleep(1)
            conn.close()

        except KeyboardInterrupt:
            print("\n[-] Shutting down honeypot.")
            break


if __name__ == "__main__":
    start_honeypot()
