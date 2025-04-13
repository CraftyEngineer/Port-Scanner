import socket
import threading
from colorama import Fore, Style, init

init(autoreset=True)

target = input("Enter target host: ")
start_port = int(input("Enter start port: "))
end_port = int(input("Enter end port: "))

print_lock = threading.Lock()

def scan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((target, port))
    with print_lock:
        if result == 0:
            print(f"{Fore.GREEN}[OPEN] Port {port}{Style.RESET_ALL}")
            save_result(f"Port {port} is OPEN")
        else:
            print(f"{Fore.RED}[CLOSED] Port {port}{Style.RESET_ALL}")
            save_result(f"Port {port} is CLOSED")
    s.close()

def save_result(message):
    with open("scan_results.txt", "a") as file:
        file.write(message + "\n")

print(f"\nStarting multithreaded scan on {target} from port {start_port} to {end_port}...\n")

for port in range(start_port, end_port + 1):
    t = threading.Thread(target=scan, args=(port,))
    t.start()
