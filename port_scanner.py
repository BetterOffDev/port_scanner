import socket
from datetime import datetime

COMMON_PORTS = [22, 80, 443, 3389]
OUTPUT_FILE = "scan_results.txt"

def check_port(host: str, port: int, timeout: float = 0.5) -> str:
    ## Attempts a TCP connection to host, port
    ## Returns: "OPEN", "CLOSED" or "TIMEOUT"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        result = sock.connect_ex((host, port))
        if result == 0:
            return "OPEN"
        return "CLOSED"
    except socket.timeout:
        return "TIMEOUT"
    except socket.gaierror:
        return "HOSTNAME_ERROR"
    except OSError:
        return "ERROR"
    finally:
        sock.close()

def main():
    host = input("Host (IP or Domain): ").strip()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"\nScanning {host}...\n")

    lines_to_write = []
    lines_to_write.append(f"\nScan Time: {timestamp}")
    lines_to_write.append(f"Host: {host}")

    open_count = 0
    for port in COMMON_PORTS:
        status = check_port(host, port)
        output_line = f"{port:5}  {status}"
        print(output_line)

        lines_to_write.append(output_line)

        if status == "OPEN":
            open_count += 1

    summary = f"\nOpen ports fount: {open_count}/{len(COMMON_PORTS)}"
    print("\n" + summary)
    lines_to_write.append(summary)

    with open(OUTPUT_FILE, "a") as f:
        for line in lines_to_write:
            f.write(line + "\n")

    print(f"\nResults saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()    
    