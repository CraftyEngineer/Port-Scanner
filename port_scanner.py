import asyncio
import aiohttp
import argparse
from colorama import Fore, Style, init

init(autoreset=True)


parser = argparse.ArgumentParser(description="Async Port Scanner")
parser.add_argument("--target", required=True, help="Target host (IP or domain)")
parser.add_argument("--start_port", type=int, default=1, help="Starting port number")
parser.add_argument("--end_port", type=int, default=1024, help="Ending port number")
parser.add_argument("--timeout", type=int, default=1, help="Timeout for port scanning in seconds")
parser.add_argument("--ports", nargs="*", type=int, help="List of ports to scan (e.g., 80 443)")
args = parser.parse_args()


target = args.target
start_port = args.start_port
end_port = args.end_port
timeout = args.timeout


if args.ports:
    ports_to_scan = args.ports
else:
    ports_to_scan = range(start_port, end_port + 1)


semaphore = asyncio.Semaphore(100)


async def scan_port(session, port):
    async with semaphore:
        try:
            async with session.get(f'http://{target}:{port}', timeout=timeout) as response:
                if response.status == 200:
                    print(f"{Fore.GREEN}[OPEN] Port {port}{Style.RESET_ALL}")
                    save_result(f"Port {port} is OPEN")
                else:
                    print(f"{Fore.RED}[CLOSED] Port {port}{Style.RESET_ALL}")
                    save_result(f"Port {port} is CLOSED")
        except:
            print(f"{Fore.RED}[CLOSED] Port {port}{Style.RESET_ALL}")
            save_result(f"Port {port} is CLOSED")

def save_result(message):
    with open("scan_results.txt", "a") as file:
        file.write(message + "\n")

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for port in ports_to_scan:
            tasks.append(scan_port(session, port))
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    print(f"\nStarting async scan on {target} from port {start_port} to {end_port}...\n")
    asyncio.run(main())
