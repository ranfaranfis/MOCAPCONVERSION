#!/usr/bin/env python3
"""
Final demonstration script showing all features of the Motion Capture GUI Converter
"""

import tkinter as tk
import os
import time
import subprocess
import json
from mocap_gui import MotionCaptureConverter

class GUIDemo:
    def __init__(self):
        self.screenshot_count = 0
        
    def take_screenshot(self, root, name_suffix=""):
        """Take a screenshot with automatic numbering."""
        try:
            self.screenshot_count += 1
            filename_base = f"demo_{self.screenshot_count:02d}_{name_suffix}" if name_suffix else f"demo_{self.screenshot_count:02d}"
            
            # Update to ensure everything is rendered
            root.update()
            time.sleep(0.5)  # Small delay for rendering
            
            x = root.winfo_rootx()
            y = root.winfo_rooty()
            width = root.winfo_width()
            height = root.winfo_height()
            
            print(f"Taking screenshot {self.screenshot_count}: {filename_base} ({width}x{height})")
            
            # Use xwd to capture the window
            xwd_file = f"{filename_base}.xwd"
            png_file = f"{filename_base}.png"
            
            result = subprocess.run([
                'xwd', '-name', 'Motion Capture CSV Converter', '-out', xwd_file
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                # Convert to PNG
                subprocess.run(['convert', xwd_file, png_file], capture_output=True)
                print(f"  ✓ Saved: {png_file}")
                return True
            else:
                print(f"  ❌ Screenshot failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"  ❌ Screenshot error: {e}")
            return False

def demonstrate_application():
    """Complete demonstration of the application features."""
    
    print("🚀 Starting Motion Capture CSV Converter Demonstration...")
    
    # Set up virtual display
    os.environ['DISPLAY'] = ':99'
    
    demo = GUIDemo()
    
    # Create main window
    root = tk.Tk()
    app = MotionCaptureConverter(root)
    
    print("\n1. 📱 Initial Application State")
    root.update()
    demo.take_screenshot(root, "initial_state")
    
    # Load CSV file
    csv_file = "20250523_170050_blendshape_data.csv"
    if os.path.exists(csv_file):
        print(f"\n2. 📁 Loading CSV file: {csv_file}")
        app.load_csv_file(csv_file)
        root.update()
        demo.take_screenshot(root, "csv_loaded")
        
        print(f"   ✓ Loaded {app.max_frames + 1} frames")
        
        # Show different frames
        print(f"\n3. 🎞️  Frame Navigation")
        
        # Frame 0 (start)
        app.frame_var.set(0)
        app.on_frame_change(0)
        root.update()
        demo.take_screenshot(root, "frame_000")
        print(f"   ✓ Frame 0: {len(app.processed_data.get('bones', {}))} bones")
        
        # Frame with significant data
        target_frame = min(50, app.max_frames)
        app.frame_var.set(target_frame)
        app.on_frame_change(target_frame)
        root.update()
        demo.take_screenshot(root, f"frame_{target_frame:03d}")
        print(f"   ✓ Frame {target_frame}: {len(app.processed_data.get('bones', {}))} bones")
        
        # Test source filtering
        print(f"\n4. 🔍 Source Filtering")
        
        # Set back to a good frame
        app.frame_var.set(10)
        app.on_frame_change(10)
        
        # Show all sources
        app.source_var.set("all")
        app.on_source_change()
        root.update()
        demo.take_screenshot(root, "filter_all")
        all_bones = len(app.processed_data.get('bones', {}))
        print(f"   ✓ All sources: {all_bones} bones")
        
        # Show face_cap only
        app.source_var.set("face_cap")
        app.on_source_change()
        root.update()
        demo.take_screenshot(root, "filter_face_cap")
        face_cap_bones = len(app.processed_data.get('bones', {}))
        print(f"   ✓ Face cap only: {face_cap_bones} bones")
        
        # Show epic only
        app.source_var.set("epic")
        app.on_source_change()
        root.update()
        demo.take_screenshot(root, "filter_epic")
        epic_bones = len(app.processed_data.get('bones', {}))
        print(f"   ✓ Epic only: {epic_bones} bones")
        
        # Show a2f only
        app.source_var.set("a2f")
        app.on_source_change()
        root.update()
        demo.take_screenshot(root, "filter_a2f")
        a2f_bones = len(app.processed_data.get('bones', {}))
        print(f"   ✓ A2F only: {a2f_bones} bones")
        
        # Back to all for export
        app.source_var.set("all")
        app.on_source_change()
        root.update()
        
        # Test JSON export
        print(f"\n5. 💾 JSON Export")
        export_file = "demo_export.json"
        
        if app.processed_data:
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(app.processed_data, f, indent=2, ensure_ascii=False)
            
            app.export_status_label.config(text=f"Exported: {export_file}")
            root.update()
            demo.take_screenshot(root, "json_exported")
            
            print(f"   ✓ Exported to {export_file}")
            
            # Show export file structure
            with open(export_file, 'r') as f:
                data = json.load(f)
                print(f"   ✓ Export contains:")
                print(f"      - Frame: {data.get('frame')}")
                print(f"      - Timecode: {data.get('timecode')}")
                print(f"      - Bones: {len(data.get('bones', {}))}")
                
                # Show sample bone data
                if 'bones' in data and data['bones']:
                    bone_name = list(data['bones'].keys())[0]
                    bone_data = data['bones'][bone_name]
                    transforms = bone_data.get('transforms', {})
                    print(f"      - Sample bone '{bone_name}': {len(transforms)} transforms")
    
    else:
        print(f"❌ CSV file not found: {csv_file}")
    
    print(f"\n6. 🏁 Demonstration Complete")
    demo.take_screenshot(root, "final_state")
    
    # Close application
    root.destroy()
    
    print(f"\n🎉 Demonstration completed successfully!")
    print(f"📸 Generated {demo.screenshot_count} screenshots")
    print(f"📁 Check the following files:")
    
    # List generated files
    for i in range(1, demo.screenshot_count + 1):
        png_file = f"demo_{i:02d}_*.png"
        print(f"   - Screenshot {i}: demo_{i:02d}_*.png")
    
    if os.path.exists("demo_export.json"):
        print(f"   - Export example: demo_export.json")

if __name__ == "__main__":
    demonstrate_application()