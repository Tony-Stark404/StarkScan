#!/usr/bin/env python3
# Simple usage banner for network_scanner (Mr. Stark style)

banner = r"""
.-"""-.
 /  .-.  \
|  /   \  |
| |(o o)| |
| |  ^  | |
 \ '---' /
  '-._.-'   MR STARK
"""

usage = """Usage: python3 network_scanner.py <target> <start_port> <end_port>
Positional: <target>=IP/hostname/CIDR    <start_port>,<end_port>=1-65535
Quick flags: --threads N   --timeout S   --ping   --json   -o OUTPUT
Example: python3 network_scanner.py 192.168.1.10 1 1024 --threads 200
"""

print(banner + "\n" + usage)
