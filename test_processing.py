#!/usr/bin/env python3
"""
Test script to demonstrate CSV loading, processing, and JSON export
"""

import os
import sys
import json
from mocap_gui import MotionCaptureConverter
import tkinter as tk

def test_processing_and_export():
    """Test the processing logic without GUI."""
    print("Testing Motion Capture CSV Processing...")
    
    # Create a minimal tkinter root for the class (it's needed for some widgets)
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    # Create the converter
    app = MotionCaptureConverter(root)
    
    # Load the CSV file
    csv_file = "20250523_170050_blendshape_data.csv"
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found")
        return
    
    try:
        app.load_csv_file(csv_file)
        print(f"✓ Successfully loaded CSV file: {csv_file}")
        print(f"✓ Number of frames: {app.max_frames + 1}")
        
        # Test different frames
        test_frames = [0, 3, 10, 50] if app.max_frames >= 50 else [0, 3, min(10, app.max_frames)]
        
        for frame_num in test_frames:
            if frame_num <= app.max_frames:
                app.current_frame = frame_num
                app.process_current_frame()
                
                bones_count = len(app.processed_data.get('bones', {}))
                print(f"✓ Frame {frame_num}: {bones_count} bones processed")
                
                if bones_count > 0:
                    # Show some sample data
                    print(f"   Sample bones: {list(app.processed_data['bones'].keys())[:3]}")
        
        # Test source filtering
        print("\nTesting source filters:")
        app.current_frame = 3
        
        for source in ['all', 'face_cap', 'epic', 'a2f']:
            app.source_filter = source
            app.process_current_frame()
            bones_count = len(app.processed_data.get('bones', {}))
            print(f"✓ Source '{source}': {bones_count} bones")
        
        # Test JSON export (simulate)
        app.source_filter = 'all'
        app.process_current_frame()
        
        export_data = app.processed_data
        if export_data:
            # Save to a test file
            test_export_file = "test_export.json"
            with open(test_export_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            print(f"✓ JSON export test successful: {test_export_file}")
            print(f"✓ Export contains {len(export_data.get('bones', {}))} bones")
            
            # Show structure
            if 'bones' in export_data:
                sample_bone = next(iter(export_data['bones'].values()))
                print(f"✓ Sample bone structure: object={sample_bone.get('object')}, transforms={len(sample_bone.get('transforms', {}))}")
        
        print("\n🎉 All tests passed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
    
    root.destroy()

if __name__ == "__main__":
    test_processing_and_export()