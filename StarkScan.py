#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                              NETWORK SCANNER                                 ║
║                    Penetration Testing Utility Tool                          ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Created by: Mr Stark                                                        ║
║  Description: Multi-threaded TCP port scanner with service detection         ║
║  Usage: python3 network_scanner.py <target> <start_port> <end_port>          ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import socket
import threading
import sys
from datetime import datetime

class NetworkScanner:
    def __init__(self, target, start_port=1, end_port=1024):
        self.target = socket.gethostbyname(target)
        self.start_port = start_port
        self.end_port = end_port
        self.open_ports = []
        self.lock = threading.Lock()
    
    def scan_port(self, port):
        """Scan a single port on the target"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.target, port))
            
            if result == 0:
                service = self.get_service_name(port)
                with self.lock:
                    self.open_ports.append((port, service))
                    print(f"  Port {port:<5} : Open  ({service})")
            
            sock.close()
        except KeyboardInterrupt:
            print("\n[!] Scan interrupted by user")
            sys.exit()
        except socket.gaierror:
            print("[!] Hostname could not be resolved")
            sys.exit()
        except socket.error:
            print("[!] Couldn't connect to server")
            sys.exit()
    
    def get_service_name(self, port):
        """Get service name for a port number"""
        try:
            return socket.getservbyport(port)
        except:
            return "Unknown Service"
    
    def scan(self):
        """Perform the port scan with formatted output"""
        print("┌" + "─" * 60 + "┐")
        print("│" + " " * 20 + "SCANNING TARGET" + " " * 20 + "│")
        print("├" + "─" * 60 + "┤")
        print(f"│ Target IP       : {self.target:<39} │")
        print(f"│ Port Range      : {self.start_port}-{self.end_port:<39} │")
        print(f"│ Start Time      : {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<39} │")
        print("└" + "─" * 60 + "┘")
        print("\n[+] Scanning in progress...")
        
        threads = []
        
        # Create threads for each port
        for port in range(self.start_port, self.end_port + 1):
            t = threading.Thread(target=self.scan_port, args=(port,))
            threads.append(t)
            t.start()
            
            # Limit concurrent threads to prevent overwhelming the system
            if len(threads) >= 100:
                for thread in threads:
                    thread.join()
                threads = []
        
        # Wait for remaining threads to complete
        for thread in threads:
            thread.join()
        
        # Print results
        print("\n┌" + "─" * 60 + "┐")
        print("│" + " " * 22 + "SCAN RESULTS" + " " * 23 + "│")
        print("├" + "─" * 60 + "┤")
        print(f"│ Finish Time     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<39} │")
        print(f"│ Open Ports      : {len(self.open_ports):<39} │")
        print("└" + "─" * 60 + "┘")
        
        if self.open_ports:
            print("\n[+] Open Ports Details:")
            print("┌──────┬──────────────────────────────────┐")
            print("│ Port │ Service                          │")
            print("├──────┼──────────────────────────────────┤")
            
            for port, service in sorted(self.open_ports):
                print(f"│ {port:<4} │ {service:<32} │")
                
            print("└──────┴──────────────────────────────────┘")
        else:
            print("\n[!] No open ports found")

def display_banner():
    """Display the tool banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║  ███╗   ██╗ ██████╗ ████████╗██╗  ██╗███████╗██████╗         ║
    ║  ████╗  ██║██╔═══██╗╚══██╔══╝██║  ██║██╔════╝██╔══██╗        ║
    ║  ██╔██╗ ██║██║   ██║   ██║   ███████║█████╗  ██████╔╝        ║
    ║  ██║╚██╗██║██║   ██║   ██║   ██╔══██║██╔══╝  ██╔══██╗        ║
    ║  ██║ ╚████║╚██████╔╝   ██║   ██║  ██║███████╗██║  ██║        ║
    ║  ╚═╝  ╚═══╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝        ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║           Advanced Network Port Scanner v1.0                  ║
    ║                 Created by: Mr Stark                          ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    display_banner()
    
    if len(sys.argv) != 4:
        print("┌" + "─" * 50 + "┐")
        print("│" + " " * 16 + "USAGE INSTRUCTIONS" + " " * 16 + "│")
        print("├" + "─" * 50 + "┤")
        print("│ python3 network_scanner.py <target> <start_port> <end_port> │")
        print("├" + "─" * 50 + "┤")
        print("│ Example: python3 network_scanner.py scanme.nmap.org 1 1000  │")
        print("└" + "─" * 50 + "┘")
        sys.exit(1)
    
    target = sys.argv[1]
    start_port = int(sys.argv[2])
    end_port = int(sys.argv[3])
    
    scanner = NetworkScanner(target, start_port, end_port)
    scanner.scan()

if __name__ == "__main__":
    main()
