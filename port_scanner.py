import asyncio
import aiohttp
from colorama import Fore, Style, init

init(autoreset=True)

target = input("Enter target host: ")
start_port = int(input("Enter start port: "))
end_port = int(input("Enter end port: "))

semaphore = asyncio.Semaphore(100)  


async def scan_port(session, port):
    async with semaphore:
        try:
            async with session.get(f'http://{target}:{port}', timeout=1) as response:
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
        for port in range(start_port, end_port + 1):
            tasks.append(scan_port(session, port))
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    print(f"\nStarting async scan on {target} from port {start_port} to {end_port}...\n")
    asyncio.run(main())
