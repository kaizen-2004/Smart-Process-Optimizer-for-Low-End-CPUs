#!/usr/bin/env python3
"""
CPU Stress Test for Arch (No Dependencies)
"""

import multiprocessing
import time

def cpu_intensive():
    """Consume CPU cycles"""
    while True:
        # Mathematical operations
        result = 0
        for i in range(10**6):
            result += i * i

def start_cpu_stress(cores=None):
    if cores is None:
        import os
        cores = os.cpu_count()
    
    print(f"🔥 Starting CPU stress on {cores} cores")
    print("📢 Buzzer should activate when CPU > 80%")
    
    processes = []
    for i in range(cores):
        p = multiprocessing.Process(target=cpu_intensive)
        p.start()
        processes.append(p)
        print(f"✅ Started worker {i+1}")
    
    return processes

if __name__ == "__main__":
    print("CPU Stress Test - Press Ctrl+C to stop")
    
    try:
        processes = start_cpu_stress()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for p in processes:
            p.terminate()
        print("🛑 Stress test stopped")