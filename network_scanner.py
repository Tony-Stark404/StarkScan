#!/usr/bin/env python3
"""
Network Scanner for Penetration Testing
Author: HackerAI
Description: TCP port scanner with threading and service detection
"""

import socket
import threading
import sys
from datetime import datetime

class NetworkScanner:
    def __init__(self, target, start_port=1, end_port=1024):
        self.target = socket.gethostbyname(target)  # Convert domain to IP
        self.start_port = start_port
        self.end_port = end_port
        self.open_ports = []
        self.lock = threading.Lock()  # For thread-safe operations
    
    def scan_port(self, port):
        """Scan a single port on the target"""
        try:
            # Create a socket object
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  # 1 second timeout
            
            # Attempt connection
            result = sock.connect_ex((self.target, port))
            
            if result == 0:
                # Port is open
                service = self.get_service_name(port)
                with self.lock:
                    self.open_ports.append((port, service))
                    print(f"Port {port}: Open ({service})")
            
            sock.close()
        except KeyboardInterrupt:
            print("\nScan interrupted by user")
            sys.exit()
        except socket.gaierror:
            print("Hostname could not be resolved")
            sys.exit()
        except socket.error:
            print("Couldn't connect to server")
            sys.exit()
    
    def get_service_name(self, port):
        """Get service name for a port number"""
        try:
            return socket.getservbyport(port)
        except:
            return "Unknown"
    
    def scan(self):
        """Perform the port scan"""
        print("-" * 50)
        print(f"Scanning target: {self.target}")
        print(f"Port range: {self.start_port}-{self.end_port}")
        print(f"Starting scan at: {datetime.now()}")
        print("-" * 50)
        
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
        print("-" * 50)
        print(f"Scan completed at: {datetime.now()}")
        print(f"Found {len(self.open_ports)} open ports")
        
        if self.open_ports:
            print("\nOpen Ports:")
            for port, service in self.open_ports:
                print(f"  {port}/tcp  {service}")
        else:
            print("No open ports found")

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 network_scanner.py <target> <start_port> <end_port>")
        print("Example: python3 network_scanner.py scanme.nmap.org 1 1000")
        sys.exit(1)
    
    target = sys.argv[1]
    start_port = int(sys.argv[2])
    end_port = int(sys.argv[3])
    
    scanner = NetworkScanner(target, start_port, end_port)
    scanner.scan()

if __name__ == "__main__":
    main()
