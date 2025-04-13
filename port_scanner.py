import tkinter as tk
from tkinter import ttk
import asyncio
import aiohttp
from colorama import Fore, Style, init

init(autoreset=True)

async def scan_port(session, target, port, timeout, result_text):
    try:
        async with session.get(f'http://{target}:{port}', timeout=timeout) as response:
            if response.status == 200:
                result_text.insert(tk.END, f"{Fore.GREEN}[OPEN] Port {port}\n")
            else:
                result_text.insert(tk.END, f"{Fore.RED}[CLOSED] Port {port}\n")
    except:
        result_text.insert(tk.END, f"{Fore.RED}[CLOSED] Port {port}\n")

async def start_scan(target, start_port, end_port, timeout, ports_to_scan, result_text):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for port in ports_to_scan:
            tasks.append(scan_port(session, target, port, timeout, result_text))
        await asyncio.gather(*tasks)

def run_scan():
    target = target_entry.get()
    start_port = int(start_port_entry.get())
    end_port = int(end_port_entry.get())
    timeout = float(timeout_entry.get())
    ports_to_scan = list(range(start_port, end_port + 1))

    result_text.delete(1.0, tk.END)  
    result_text.insert(tk.END, f"Starting scan on {target} from port {start_port} to {end_port}...\n")
    asyncio.run(start_scan(target, start_port, end_port, timeout, ports_to_scan, result_text))

root = tk.Tk()
root.title("Async Port Scanner")

target_label = ttk.Label(root, text="Target:")
target_label.grid(row=0, column=0, padx=10, pady=10)
target_entry = ttk.Entry(root, width=30)
target_entry.grid(row=0, column=1, padx=10, pady=10)

start_port_label = ttk.Label(root, text="Start Port:")
start_port_label.grid(row=1, column=0, padx=10, pady=10)
start_port_entry = ttk.Entry(root, width=10)
start_port_entry.grid(row=1, column=1, padx=10, pady=10)

end_port_label = ttk.Label(root, text="End Port:")
end_port_label.grid(row=2, column=0, padx=10, pady=10)
end_port_entry = ttk.Entry(root, width=10)
end_port_entry.grid(row=2, column=1, padx=10, pady=10)

timeout_label = ttk.Label(root, text="Timeout (sec):")
timeout_label.grid(row=3, column=0, padx=10, pady=10)
timeout_entry = ttk.Entry(root, width=10)
timeout_entry.grid(row=3, column=1, padx=10, pady=10)

scan_button = ttk.Button(root, text="Start Scan", command=run_scan)
scan_button.grid(row=4, column=0, columnspan=2, padx=10, pady=20)

result_text = tk.Text(root, width=50, height=15)
result_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
