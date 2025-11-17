#!/usr/bin/env python3
"""
Process Optimizer with System Monitoring
Sends CPU and RAM usage to Arduino via JSON
"""

import psutil
import json
import time
import serial
import os

class ProcessOptimizer:
    def __init__(self, serial_port='/dev/ttyACM0', baudrate=9600):
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.ser = None
        
    def connect_arduino(self):
        """Connect to Arduino serial port"""
        try:
            self.ser = serial.Serial(self.serial_port, self.baudrate, timeout=1)
            time.sleep(2)  # Wait for Arduino to reset
            print(f"Connected to Arduino on {self.serial_port}")
            return True
        except serial.SerialException as e:
            print(f"Error connecting to Arduino: {e}")
            return False
    
    def get_system_usage(self):
        """Get current CPU and RAM usage"""
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        return cpu_usage, ram_usage
    
    def generate_json_data(self, cpu_usage, ram_usage):
        """Generate JSON data with system usage"""
        data = {
            "cpu_usage": round(cpu_usage, 1),
            "ram_usage": round(ram_usage, 1),
            "timestamp": time.time()
        }
        return json.dumps(data)
    
    def save_to_json_file(self, data, filename="system_stats.json"):
        """Save data to JSON file"""
        with open(filename, 'w') as f:
            json.dump(json.loads(data), f, indent=2)
        print(f"Data saved to {filename}")
    
    def run(self):
        """Main monitoring loop"""
        if not self.connect_arduino():
            return
        
        print("Starting system monitoring...")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                # Get system usage
                cpu_usage, ram_usage = self.get_system_usage()
                
                # Generate JSON data
                json_data = self.generate_json_data(cpu_usage, ram_usage)
                
                # Save to file
                self.save_to_json_file(json_data)
                
                # Send to Arduino
                if self.ser and self.ser.is_open:
                    self.ser.write((json_data + '\n').encode())
                    print(f"Sent: CPU {cpu_usage:.1f}%, RAM {ram_usage:.1f}%")
                
                # Wait before next reading
                time.sleep(2)
                
        except KeyboardInterrupt:
            print("\nStopping monitoring...")
        finally:
            if self.ser and self.ser.is_open:
                self.ser.close()

if __name__ == "__main__":
    # Adjust the serial port based on your system
    # Windows: 'COM3', Linux: '/dev/ttyACM0', macOS: '/dev/cu.usbmodemXXXX'
    optimizer = ProcessOptimizer(serial_port='/dev/ttyACM0')  # Change this!
    optimizer.run()