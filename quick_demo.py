#!/usr/bin/env python3
"""
Quick demo script to test a few known IP ranges
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ethereum_node_scanner import EthereumNodeScanner

def main():
    print("🚀 Quick Demo - Ethereum Node Scanner")
    print("=" * 50)
    
    # Create scanner with high performance settings
    scanner = EthereumNodeScanner(timeout=2, max_threads=500)
    
    # Test public IP ranges from Asia and Europe
    test_ranges = [
        "1.0.0.0/16",       # APNIC - Asia Pacific
        "2.0.0.0/16",       # RIPE NCC - Europe
        "5.0.0.0/16",       # RIPE NCC - Europe
        "14.0.0.0/16",      # APNIC - Asia Pacific
        "27.0.0.0/16",      # APNIC - Asia Pacific
        "31.0.0.0/16",      # RIPE NCC - Europe
        "36.0.0.0/16",      # APNIC - Asia Pacific
        "46.0.0.0/16",      # RIPE NCC - Europe
        "51.0.0.0/16",      # RIPE NCC - Europe
        "58.0.0.0/16",      # APNIC - Asia Pacific
        "77.0.0.0/16",      # RIPE NCC - Europe
        "80.0.0.0/16",      # RIPE NCC - Europe
        "101.0.0.0/16",     # APNIC - Asia Pacific
        "103.0.0.0/16",     # APNIC - Asia Pacific
        "110.0.0.0/16",     # APNIC - Asia Pacific
        "128.0.0.0/16",     # RIPE NCC - Europe
        "129.0.0.0/16",     # RIPE NCC - Europe
        "130.0.0.0/16",     # RIPE NCC - Europe
        "175.0.0.0/16",     # APNIC - Asia Pacific
        "180.0.0.0/16",     # APNIC - Asia Pacific
        "193.0.0.0/16",     # RIPE NCC - Europe
        "202.0.0.0/16",     # APNIC - Asia Pacific
        "210.0.0.0/16",     # APNIC - Asia Pacific
        "218.0.0.0/16",     # APNIC - Asia Pacific
    ]
    
    print("Testing public IP ranges from Asia and Europe...")
    for network in test_ranges:
        print(f"\n🔍 Scanning {network}...")
        scanner.scan_network_range(network)
    
    # Print results
    scanner.print_summary()
    
    if scanner.found_nodes:
        filename = scanner.save_results("quick_demo_results.json")
        print(f"\n📁 Results saved to: {filename}")
        
        print("\n🎯 Found Ethereum nodes:")
        for i, node in enumerate(scanner.found_nodes, 1):
            print(f"  {i}. {node['ip']}:{node['port']}")
            syncing = node['response'].get('result', 'unknown')
            print(f"     Syncing: {syncing}")
    else:
        print("\n❌ No Ethereum nodes found in test ranges")
        print("💡 Try running the full scan with: python3 ethereum_node_scanner.py --asia-europe --threads 2000")

if __name__ == "__main__":
    main()
