import socket
from datetime import datetime

COMMON_PORTS = [
    21,    # FTP
    22,    # SSH
    23,    # Telnet
    25,    # SMTP
    53,    # DNS
    67, 68,# DHCP
    69,    # TFTP
    80,    # HTTP
    110,   # POP3
    123,   # NTP
    135,   # MS RPC
    137, 138, 139,  # NetBIOS
    143,   # IMAP
    161,   # SNMP
    389,   # LDAP
    443,   # HTTPS
    445,   # SMB
    587,   # SMTP submission
    993,   # IMAPS
    995,   # POP3S
    1433,  # MSSQL
    1521,  # Oracle
    2049,  # NFS
    3306,  # MySQL
    3389,  # RDP
    5432,  # PostgreSQL
    5900,  # VNC
    6379,  # Redis
    8080   # Alternate HTTP
]

OUTPUT_FILE = "scan_results.txt"

def check_port(host: str, port: int, timeout: float = 0.5) -> str:
    ## Attempts a TCP connection to host, port
    ## Returns: "OPEN", "CLOSED" or "TIMEOUT"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        with socket.create_connection((host, port), timeout=timeout):
            return "OPEN"
        return "CLOSED"
    except socket.timeout:
        return "TIMEOUT"
    except socket.gaierror:
        return "HOSTNAME_ERROR"
    except ConnectionRefusedError:
        return "CLOSED"
    except OSError:
        return "ERROR"
        #Covers "Network is unreachable", "No route to host", etc.
    finally:
        sock.close()

def get_service_name(port: int) -> str:
    ##Ask the OS for the known service name. Falls back to "unknown" if not defined
    try:
        return socket.getservbyport(port, "tcp")
    except OSError:
        return "unknown"

def main():
    host = input("Host (IP or Domain): ").strip()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"\nScanning {host}...\n")

    lines_to_write = [
        f"Scan Time: {timestamp}",
        f"Host: {host}",
        "PORT   SERVICE        STATUS",
        "-" * 30,
    ]

    open_count = 0
    for port in COMMON_PORTS:
        service = get_service_name(port)
        status = check_port(host, port)
        output_line = f"{port:5}  {service: <12} {status}"
        print(output_line)

        lines_to_write.append(output_line)

        if status == "OPEN":
            open_count += 1

    summary = f"Open ports found: {open_count}/{len(COMMON_PORTS)}"
    print("\n" + summary)
    lines_to_write.append(summary)

    with open(OUTPUT_FILE, "a") as f:
        for line in lines_to_write:
            f.write(line + "\n")

    print(f"\nResults saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()    
    