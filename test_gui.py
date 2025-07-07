#!/usr/bin/env python3
"""
Test script to run the GUI application and take a screenshot
"""

import tkinter as tk
import os
import time
from mocap_gui import MotionCaptureConverter

def test_gui():
    # Set up virtual display if needed
    os.environ['DISPLAY'] = ':99'
    
    # Create main window
    root = tk.Tk()
    
    # Initialize the application
    app = MotionCaptureConverter(root)
    
    # Update the GUI to ensure it's rendered
    root.update()
    
    # Take a screenshot after a short delay
    root.after(1000, lambda: take_screenshot_and_exit(root))
    
    # Run the main loop
    root.mainloop()

def take_screenshot_and_exit(root):
    try:
        # Try to take a screenshot using tkinter's built-in functionality
        x = root.winfo_rootx()
        y = root.winfo_rooty()
        width = root.winfo_width()
        height = root.winfo_height()
        
        print(f"Window dimensions: {width}x{height} at ({x}, {y})")
        
        # Import screenshot tools
        import subprocess
        
        # Use xwd to capture the window
        result = subprocess.run([
            'xwd', '-name', 'Motion Capture CSV Converter', '-out', 'gui_screenshot.xwd'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Screenshot saved as gui_screenshot.xwd")
            # Convert to PNG if imagemagick is available
            subprocess.run(['convert', 'gui_screenshot.xwd', 'gui_screenshot.png'], 
                         capture_output=True)
        else:
            print("Screenshot failed:", result.stderr)
            
    except Exception as e:
        print(f"Screenshot error: {e}")
    
    # Close the application
    root.destroy()

if __name__ == "__main__":
    test_gui()