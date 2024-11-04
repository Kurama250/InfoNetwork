# Create by Github.com/Kurama250
# pip install psutil colorama

import psutil
import time
import os
from colorama import Fore, init

init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def format_bytes(byte_size):
    if byte_size < 1024:
        return f"{byte_size} B"
    elif byte_size < 1048576:
        return f"{byte_size / 1024:.2f} KB"
    elif byte_size < 1073741824:
        return f"{byte_size / 1048576:.2f} MB"
    else:
        return f"{byte_size / 1073741824:.2f} GB"

def get_network_usage():
    network_usage = {}
    for conn in psutil.net_connections(kind='inet'):
        try:
            pid = conn.pid
            if pid:
                process = psutil.Process(pid)
                name = process.name()
                bytes_sent, bytes_recv = process.io_counters()[:2]

                if name not in network_usage:
                    network_usage[name] = {'sent': 0, 'recv': 0}
                
                network_usage[name]['sent'] += bytes_sent
                network_usage[name]['recv'] += bytes_recv
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return network_usage

while True:
    clear_screen()
    print(Fore.CYAN + "\nNetwork Usage by Program (refreshed every 5 seconds):")
    print(Fore.GREEN + "{:<45} {:<15} {:<15}".format("Program", "Sent", "Received"))
    print(Fore.WHITE + "-" * 75)

    network_usage = get_network_usage()

    sorted_usage = sorted(network_usage.items(), key=lambda x: x[1]['recv'], reverse=True)

    for name, usage in sorted_usage:
        sent_color = Fore.YELLOW if usage['sent'] > 0 else Fore.WHITE
        recv_color = Fore.RED if usage['recv'] > 0 else Fore.WHITE
        print(f"{sent_color}{name:<45} {sent_color}{format_bytes(usage['sent']):<15} {recv_color}{format_bytes(usage['recv']):<15}")

    print(Fore.WHITE + "-" * 75)
    time.sleep(5)

input(Fore.MAGENTA + "Press Enter to close...")