import socket

target = "google.com"
port = 80

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)  # optional timeout in seconds

result = s.connect_ex((target, port))

if result == 0:
    print(f"Port {port} is open")
else:
    print(f"Port {port} is closed")

s.close()
