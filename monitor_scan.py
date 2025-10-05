#!/usr/bin/env python3
"""
Monitor script to check scan progress and results
"""

import os
import json
import time
import glob
from datetime import datetime

def monitor_scan():
    print("🔍 Ethereum Node Scanner Monitor")
    print("=" * 50)
    
    while True:
        # Check for result files
        result_files = glob.glob("ethereum_nodes_*.json")
        
        if result_files:
            # Get the latest file
            latest_file = max(result_files, key=os.path.getctime)
            
            try:
                with open(latest_file, 'r') as f:
                    data = json.load(f)
                
                print(f"\n📊 Latest Results from: {latest_file}")
                print(f"⏰ Scan Time: {data.get('scan_time', 'Unknown')}")
                print(f"🎯 Total Nodes Found: {data.get('total_nodes_found', 0)}")
                
                if data.get('nodes'):
                    print(f"\n🌐 Found Ethereum Nodes:")
                    for i, node in enumerate(data['nodes'][:10], 1):  # Show first 10
                        syncing = node['response'].get('result', 'unknown')
                        print(f"  {i:2d}. {node['ip']}:{node['port']} - Syncing: {syncing}")
                    
                    if len(data['nodes']) > 10:
                        print(f"  ... and {len(data['nodes']) - 10} more nodes")
                
            except Exception as e:
                print(f"Error reading results: {e}")
        else:
            print("⏳ No scan results found yet...")
        
        print(f"\n🔄 Last checked: {datetime.now().strftime('%H:%M:%S')}")
        print("Press Ctrl+C to stop monitoring")
        
        try:
            time.sleep(30)  # Check every 30 seconds
        except KeyboardInterrupt:
            print("\n👋 Monitoring stopped")
            break

if __name__ == "__main__":
    monitor_scan()
