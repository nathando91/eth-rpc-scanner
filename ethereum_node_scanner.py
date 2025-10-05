#!/usr/bin/env python3
"""
Ethereum Node Scanner
Scans for Ethereum nodes running on port 8545 that respond to eth_syncing JSON-RPC calls
"""

import socket
import json
import requests
import threading
import time
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import argparse
import sys

class EthereumNodeScanner:
    def __init__(self, timeout=3, max_threads=1000):
        self.timeout = timeout
        self.max_threads = max_threads
        self.found_nodes = []
        self.lock = threading.Lock()
        
    def is_port_open(self, ip, port=8545):
        """Check if a port is open on the given IP"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def test_ethereum_node(self, ip, port=8545):
        """Test if the IP responds to Ethereum JSON-RPC eth_syncing call"""
        try:
            url = f"http://{ip}:{port}"
            payload = {
                "jsonrpc": "2.0",
                "method": "eth_syncing",
                "params": [],
                "id": 1
            }
            
            response = requests.post(
                url, 
                json=payload, 
                timeout=self.timeout,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                # Check if it's a valid JSON-RPC response
                if "jsonrpc" in data and "id" in data:
                    return {
                        "ip": ip,
                        "port": port,
                        "response": data,
                        "status": "active"
                    }
        except Exception as e:
            pass
        return None
    
    def scan_ip(self, ip):
        """Scan a single IP address"""
        if self.is_port_open(ip, 8545):
            node_info = self.test_ethereum_node(ip, 8545)
            if node_info:
                with self.lock:
                    self.found_nodes.append(node_info)
                    print(f"✓ Found Ethereum node: {ip}:8545")
                    print(f"  Response: {node_info['response']}")
                    # Auto-save results when new node is found
                    self.auto_save_results()
                return node_info
        return None
    
    def scan_network_range(self, network):
        """Scan a network range for Ethereum nodes"""
        print(f"Scanning network: {network}")
        try:
            network_obj = ipaddress.ip_network(network, strict=False)
            ips = [str(ip) for ip in network_obj.hosts()]
            
            with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
                futures = {executor.submit(self.scan_ip, ip): ip for ip in ips}
                
                for future in as_completed(futures):
                    ip = futures[future]
                    try:
                        result = future.result()
                    except Exception as e:
                        pass
                        
        except Exception as e:
            print(f"Error scanning network {network}: {e}")
    
    def scan_common_ranges(self):
        """Scan common private network ranges"""
        common_ranges = [
            "192.168.0.0/16",    # Class C private
            "10.0.0.0/8",        # Class A private
            "172.16.0.0/12",     # Class B private
            "127.0.0.0/8",       # Loopback
        ]
        
        for network in common_ranges:
            self.scan_network_range(network)
    
    def scan_asia_europe_ranges(self):
        """Scan major Asia and Europe IP ranges"""
        # Major Asia IP ranges (using /16 instead of /8 to avoid huge scans)
        asia_ranges = [
            "1.1.0.0/16",        # APNIC - Asia Pacific
            "1.2.0.0/16",        # APNIC - Asia Pacific
            "1.3.0.0/16",        # APNIC - Asia Pacific
            "14.0.0.0/16",       # APNIC - Asia Pacific
            "14.1.0.0/16",       # APNIC - Asia Pacific
            "27.0.0.0/16",       # APNIC - Asia Pacific
            "27.1.0.0/16",       # APNIC - Asia Pacific
            "36.0.0.0/16",       # APNIC - Asia Pacific
            "36.1.0.0/16",       # APNIC - Asia Pacific
            "39.0.0.0/16",       # APNIC - Asia Pacific
            "42.0.0.0/16",       # APNIC - Asia Pacific
            "49.0.0.0/16",       # APNIC - Asia Pacific
            "58.0.0.0/16",       # APNIC - Asia Pacific
            "58.1.0.0/16",       # APNIC - Asia Pacific
            "59.0.0.0/16",       # APNIC - Asia Pacific
            "60.0.0.0/16",       # APNIC - Asia Pacific
            "60.1.0.0/16",       # APNIC - Asia Pacific
            "61.0.0.0/16",       # APNIC - Asia Pacific
            "61.1.0.0/16",       # APNIC - Asia Pacific
            "101.0.0.0/16",      # APNIC - Asia Pacific
            "101.1.0.0/16",      # APNIC - Asia Pacific
            "103.0.0.0/16",      # APNIC - Asia Pacific
            "103.1.0.0/16",      # APNIC - Asia Pacific
            "106.0.0.0/16",      # APNIC - Asia Pacific
            "110.0.0.0/16",      # APNIC - Asia Pacific
            "110.1.0.0/16",      # APNIC - Asia Pacific
            "111.0.0.0/16",      # APNIC - Asia Pacific
            "112.0.0.0/16",      # APNIC - Asia Pacific
            "113.0.0.0/16",      # APNIC - Asia Pacific
            "114.0.0.0/16",      # APNIC - Asia Pacific
            "115.0.0.0/16",      # APNIC - Asia Pacific
            "116.0.0.0/16",      # APNIC - Asia Pacific
            "117.0.0.0/16",      # APNIC - Asia Pacific
            "118.0.0.0/16",      # APNIC - Asia Pacific
            "119.0.0.0/16",      # APNIC - Asia Pacific
            "120.0.0.0/16",      # APNIC - Asia Pacific
            "121.0.0.0/16",      # APNIC - Asia Pacific
            "122.0.0.0/16",      # APNIC - Asia Pacific
            "123.0.0.0/16",      # APNIC - Asia Pacific
            "124.0.0.0/16",      # APNIC - Asia Pacific
            "125.0.0.0/16",      # APNIC - Asia Pacific
            "126.0.0.0/16",      # APNIC - Asia Pacific
            "175.0.0.0/16",      # APNIC - Asia Pacific
            "180.0.0.0/16",      # APNIC - Asia Pacific
            "182.0.0.0/16",      # APNIC - Asia Pacific
            "183.0.0.0/16",      # APNIC - Asia Pacific
            "202.0.0.0/16",      # APNIC - Asia Pacific
            "202.1.0.0/16",      # APNIC - Asia Pacific
            "203.0.0.0/16",      # APNIC - Asia Pacific
            "210.0.0.0/16",      # APNIC - Asia Pacific
            "210.1.0.0/16",      # APNIC - Asia Pacific
            "211.0.0.0/16",      # APNIC - Asia Pacific
            "218.0.0.0/16",      # APNIC - Asia Pacific
            "218.1.0.0/16",      # APNIC - Asia Pacific
            "219.0.0.0/16",      # APNIC - Asia Pacific
            "220.0.0.0/16",      # APNIC - Asia Pacific
            "221.0.0.0/16",      # APNIC - Asia Pacific
            "222.0.0.0/16",      # APNIC - Asia Pacific
            "223.0.0.0/16",      # APNIC - Asia Pacific
        ]
        
        # Major Europe IP ranges (using /16 instead of /8 to avoid huge scans)
        europe_ranges = [
            "2.0.0.0/16",        # RIPE NCC - Europe
            "2.1.0.0/16",        # RIPE NCC - Europe
            "5.0.0.0/16",        # RIPE NCC - Europe
            "5.1.0.0/16",        # RIPE NCC - Europe
            "31.0.0.0/16",       # RIPE NCC - Europe
            "31.1.0.0/16",       # RIPE NCC - Europe
            "37.0.0.0/16",       # RIPE NCC - Europe
            "46.0.0.0/16",       # RIPE NCC - Europe
            "46.1.0.0/16",       # RIPE NCC - Europe
            "51.0.0.0/16",       # RIPE NCC - Europe
            "51.1.0.0/16",       # RIPE NCC - Europe
            "62.0.0.0/16",       # RIPE NCC - Europe
            "77.0.0.0/16",       # RIPE NCC - Europe
            "77.1.0.0/16",       # RIPE NCC - Europe
            "78.0.0.0/16",       # RIPE NCC - Europe
            "79.0.0.0/16",       # RIPE NCC - Europe
            "80.0.0.0/16",       # RIPE NCC - Europe
            "80.1.0.0/16",       # RIPE NCC - Europe
            "81.0.0.0/16",       # RIPE NCC - Europe
            "82.0.0.0/16",       # RIPE NCC - Europe
            "83.0.0.0/16",       # RIPE NCC - Europe
            "84.0.0.0/16",       # RIPE NCC - Europe
            "85.0.0.0/16",       # RIPE NCC - Europe
            "86.0.0.0/16",       # RIPE NCC - Europe
            "87.0.0.0/16",       # RIPE NCC - Europe
            "88.0.0.0/16",       # RIPE NCC - Europe
            "89.0.0.0/16",       # RIPE NCC - Europe
            "90.0.0.0/16",       # RIPE NCC - Europe
            "91.0.0.0/16",       # RIPE NCC - Europe
            "92.0.0.0/16",       # RIPE NCC - Europe
            "93.0.0.0/16",       # RIPE NCC - Europe
            "94.0.0.0/16",       # RIPE NCC - Europe
            "95.0.0.0/16",       # RIPE NCC - Europe
            "109.0.0.0/16",      # RIPE NCC - Europe
            "128.0.0.0/16",      # RIPE NCC - Europe
            "128.1.0.0/16",      # RIPE NCC - Europe
            "129.0.0.0/16",      # RIPE NCC - Europe
            "130.0.0.0/16",      # RIPE NCC - Europe
            "131.0.0.0/16",      # RIPE NCC - Europe
            "132.0.0.0/16",      # RIPE NCC - Europe
            "133.0.0.0/16",      # RIPE NCC - Europe
            "134.0.0.0/16",      # RIPE NCC - Europe
            "135.0.0.0/16",      # RIPE NCC - Europe
            "136.0.0.0/16",      # RIPE NCC - Europe
            "137.0.0.0/16",      # RIPE NCC - Europe
            "137.1.0.0/16",      # RIPE NCC - Europe
            "138.0.0.0/16",      # RIPE NCC - Europe
            "139.0.0.0/16",      # RIPE NCC - Europe
            "140.0.0.0/16",      # RIPE NCC - Europe
            "141.0.0.0/16",      # RIPE NCC - Europe
            "142.0.0.0/16",      # RIPE NCC - Europe
            "143.0.0.0/16",      # RIPE NCC - Europe
            "144.0.0.0/16",      # RIPE NCC - Europe
            "145.0.0.0/16",      # RIPE NCC - Europe
            "146.0.0.0/16",      # RIPE NCC - Europe
            "147.0.0.0/16",      # RIPE NCC - Europe
            "148.0.0.0/16",      # RIPE NCC - Europe
            "149.0.0.0/16",      # RIPE NCC - Europe
            "150.0.0.0/16",      # RIPE NCC - Europe
            "151.0.0.0/16",      # RIPE NCC - Europe
            "152.0.0.0/16",      # RIPE NCC - Europe
            "153.0.0.0/16",      # RIPE NCC - Europe
            "154.0.0.0/16",      # RIPE NCC - Europe
            "155.0.0.0/16",      # RIPE NCC - Europe
            "156.0.0.0/16",      # RIPE NCC - Europe
            "157.0.0.0/16",      # RIPE NCC - Europe
            "158.0.0.0/16",      # RIPE NCC - Europe
            "159.0.0.0/16",      # RIPE NCC - Europe
            "160.0.0.0/16",      # RIPE NCC - Europe
            "161.0.0.0/16",      # RIPE NCC - Europe
            "162.0.0.0/16",      # RIPE NCC - Europe
            "163.0.0.0/16",      # RIPE NCC - Europe
            "164.0.0.0/16",      # RIPE NCC - Europe
            "165.0.0.0/16",      # RIPE NCC - Europe
            "166.0.0.0/16",      # RIPE NCC - Europe
            "167.0.0.0/16",      # RIPE NCC - Europe
            "168.0.0.0/16",      # RIPE NCC - Europe
            "169.0.0.0/16",      # RIPE NCC - Europe
            "170.0.0.0/16",      # RIPE NCC - Europe
            "171.0.0.0/16",      # RIPE NCC - Europe
            "172.0.0.0/16",      # RIPE NCC - Europe
            "173.0.0.0/16",      # RIPE NCC - Europe
            "174.0.0.0/16",      # RIPE NCC - Europe
            "176.0.0.0/16",      # RIPE NCC - Europe
            "177.0.0.0/16",      # RIPE NCC - Europe
            "178.0.0.0/16",      # RIPE NCC - Europe
            "179.0.0.0/16",      # RIPE NCC - Europe
            "181.0.0.0/16",      # RIPE NCC - Europe
            "185.0.0.0/16",      # RIPE NCC - Europe
            "188.0.0.0/16",      # RIPE NCC - Europe
            "193.0.0.0/16",      # RIPE NCC - Europe
            "193.1.0.0/16",      # RIPE NCC - Europe
            "194.0.0.0/16",      # RIPE NCC - Europe
            "195.0.0.0/16",      # RIPE NCC - Europe
            "212.0.0.0/16",      # RIPE NCC - Europe
            "212.1.0.0/16",      # RIPE NCC - Europe
            "213.0.0.0/16",      # RIPE NCC - Europe
        ]
        
        all_ranges = asia_ranges + europe_ranges
        
        print(f"Scanning {len(asia_ranges)} Asia IP ranges and {len(europe_ranges)} Europe IP ranges...")
        print("WARNING: This will scan millions of IP addresses and may take a very long time!")
        print("Press Ctrl+C to stop at any time.")
        
        for i, network in enumerate(all_ranges, 1):
            print(f"\n[{i}/{len(all_ranges)}] Scanning {network}...")
            self.scan_network_range(network)
    
    def scan_public_range(self, start_ip, end_ip):
        """Scan a specific public IP range (use with caution)"""
        try:
            start = ipaddress.ip_address(start_ip)
            end = ipaddress.ip_address(end_ip)
            
            current = start
            while current <= end:
                self.scan_ip(str(current))
                current += 1
                
        except Exception as e:
            print(f"Error scanning public range: {e}")
    
    def auto_save_results(self):
        """Auto-save results when new node is found"""
        try:
            results = {
                "scan_time": datetime.now().isoformat(),
                "total_nodes_found": len(self.found_nodes),
                "nodes": self.found_nodes
            }
            
            # Save to both current results and timestamped file
            with open("ethereum_nodes_current.json", 'w') as f:
                json.dump(results, f, indent=2)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ethereum_nodes_{timestamp}.json"
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
                
            print(f"  💾 Auto-saved to: ethereum_nodes_current.json")
            
        except Exception as e:
            print(f"  ❌ Error auto-saving: {e}")
    
    def save_results(self, filename=None):
        """Save results to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ethereum_nodes_{timestamp}.json"
        
        results = {
            "scan_time": datetime.now().isoformat(),
            "total_nodes_found": len(self.found_nodes),
            "nodes": self.found_nodes
        }
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\nResults saved to: {filename}")
        return filename
    
    def print_summary(self):
        """Print scan summary"""
        print(f"\n{'='*50}")
        print(f"SCAN SUMMARY")
        print(f"{'='*50}")
        print(f"Total Ethereum nodes found: {len(self.found_nodes)}")
        print(f"Scan completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if self.found_nodes:
            print(f"\nFound nodes:")
            for i, node in enumerate(self.found_nodes, 1):
                print(f"{i:3d}. {node['ip']}:{node['port']}")
                if 'response' in node:
                    syncing = node['response'].get('result', 'unknown')
                    print(f"     Syncing status: {syncing}")

def main():
    parser = argparse.ArgumentParser(description="Scan for Ethereum nodes on port 8545")
    parser.add_argument("--network", help="Network range to scan (e.g., 192.168.1.0/24)")
    parser.add_argument("--ip-range", nargs=2, metavar=("START", "END"), 
                       help="IP range to scan (e.g., 192.168.1.1 192.168.1.254)")
    parser.add_argument("--timeout", type=int, default=3, help="Connection timeout in seconds")
    parser.add_argument("--threads", type=int, default=1000, help="Maximum number of threads")
    parser.add_argument("--output", help="Output filename for results")
    parser.add_argument("--common", action="store_true", help="Scan common private network ranges")
    parser.add_argument("--asia-europe", action="store_true", help="Scan major Asia and Europe IP ranges (WARNING: Very large scan)")
    
    args = parser.parse_args()
    
    scanner = EthereumNodeScanner(timeout=args.timeout, max_threads=args.threads)
    
    print("Ethereum Node Scanner")
    print("=" * 50)
    print(f"Scanning for Ethereum nodes on port 8545...")
    print(f"Timeout: {args.timeout}s, Threads: {args.threads}")
    print()
    
    start_time = time.time()
    
    if args.network:
        scanner.scan_network_range(args.network)
    elif args.ip_range:
        scanner.scan_public_range(args.ip_range[0], args.ip_range[1])
    elif args.asia_europe:
        scanner.scan_asia_europe_ranges()
    elif args.common:
        scanner.scan_common_ranges()
    else:
        # Default: scan common private ranges
        print("No specific range specified, scanning common private networks...")
        scanner.scan_common_ranges()
    
    end_time = time.time()
    
    scanner.print_summary()
    
    if scanner.found_nodes:
        filename = scanner.save_results(args.output)
        print(f"\nDetailed results saved to: {filename}")
    
    print(f"\nScan completed in {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
