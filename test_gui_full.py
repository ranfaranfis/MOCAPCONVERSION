#!/usr/bin/env python3
"""
Comprehensive test script to demonstrate the GUI application with CSV loading
"""

import tkinter as tk
import os
import time
import subprocess
from mocap_gui import MotionCaptureConverter

def test_gui_with_csv():
    # Set up virtual display
    os.environ['DISPLAY'] = ':99'
    
    # Create main window
    root = tk.Tk()
    
    # Initialize the application
    app = MotionCaptureConverter(root)
    
    # Update the GUI to ensure it's rendered
    root.update()
    
    # Load the sample CSV file automatically
    csv_file = "20250523_170050_blendshape_data.csv"
    if os.path.exists(csv_file):
        try:
            app.load_csv_file(csv_file)
            print(f"Successfully loaded CSV file: {csv_file}")
            print(f"Number of frames: {app.max_frames + 1}")
            
            # Update the display
            root.update()
            
            # Set a different frame to show data
            if app.max_frames > 3:
                app.frame_var.set(3)
                app.on_frame_change(3)
                root.update()
                print(f"Set frame to 3, processed data has {len(app.processed_data.get('bones', {}))} bones")
            
        except Exception as e:
            print(f"Error loading CSV: {e}")
    
    # Take a screenshot after everything is loaded
    root.after(2000, lambda: take_screenshot_and_exit(root, "gui_with_data_screenshot"))
    
    # Run the main loop
    root.mainloop()

def take_screenshot_and_exit(root, filename_base):
    try:
        # Get window info
        x = root.winfo_rootx()
        y = root.winfo_rooty()
        width = root.winfo_width()
        height = root.winfo_height()
        
        print(f"Final window dimensions: {width}x{height} at ({x}, {y})")
        
        # Use xwd to capture the window
        xwd_file = f"{filename_base}.xwd"
        png_file = f"{filename_base}.png"
        
        result = subprocess.run([
            'xwd', '-name', 'Motion Capture CSV Converter', '-out', xwd_file
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Screenshot saved as {xwd_file}")
            # Convert to PNG
            subprocess.run(['convert', xwd_file, png_file], capture_output=True)
            print(f"Converted to {png_file}")
        else:
            print("Screenshot failed:", result.stderr)
            
    except Exception as e:
        print(f"Screenshot error: {e}")
    
    # Close the application
    root.destroy()

if __name__ == "__main__":
    test_gui_with_csv()