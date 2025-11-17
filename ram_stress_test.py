#!/usr/bin/env python3
"""
RAM Stress Test for Arch - Fixed Version
"""

import time

def stress_ram():
    print("🧠 RAM Stress Test - FIXED")
    print("📢 Buzzer should activate when RAM > 85%")
    
    # Get TOTAL memory, not available
    with open('/proc/meminfo', 'r') as f:
        meminfo = f.read()
        total_line = [line for line in meminfo.split('\n') if 'MemTotal' in line][0]
        total_kb = int(total_line.split()[1])
    
    total_gb = total_kb / 1024 / 1024
    print(f"📊 Total RAM: {total_gb:.1f}GB")
    
    # Calculate 90% of TOTAL memory to exceed 85% threshold
    target_bytes = int(total_kb * 0.85 * 1024)  # 90% of total RAM
    chunk_size = 200 * 1024 * 1024  # 200MB chunks
    
    memory_blocks = []
    allocated = 0
    
    try:
        print("📦 Allocating memory to exceed 85% threshold...")
        while allocated < target_bytes:
            try:
                # Allocate in chunks
                block = ' ' * chunk_size
                memory_blocks.append(block)
                allocated += chunk_size
                current_percent = (allocated / (total_kb * 1024)) * 100
                print(f"   Allocated: {allocated/1024/1024:.1f}MB ({current_percent:.1f}% of total)")
                time.sleep(1)  # Longer delay to see progress
                
                # Check if we've exceeded threshold
                if current_percent > 85:
                    print("🎯 EXCEEDED 85% THRESHOLD! BUZZER SHOULD ACTIVATE!")
                    
            except MemoryError:
                print("⚠️  Memory allocation limited by system")
                break
        
        final_percent = (allocated / (total_kb * 1024)) * 100
        print(f"✅ Final allocation: {allocated/1024/1024:.1f}MB ({final_percent:.1f}% of total)")
        print("⏰ Holding for 30 seconds...")
        
        # Keep checking during hold period
        for i in range(30, 0, -1):
            print(f"   {i}s remaining... BUZZER SHOULD BE ACTIVE!")
            time.sleep(1)
        
    finally:
        memory_blocks.clear()
        print("🔄 Memory released")
        print("🔇 Buzzer should stop now")

if __name__ == "__main__":
    stress_ram()