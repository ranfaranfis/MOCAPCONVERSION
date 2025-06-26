#!/usr/bin/env python3
"""
Example usage of the MOCAP to Blender converter

This example demonstrates various ways to use the optimized script generator.
"""

import os
from mocap_converter import main as converter_main
import sys

def run_example():
    """Run example conversions with different settings."""
    
    # Sample data file
    csv_file = "20250523_170050_blendshape_data.csv"
    
    if not os.path.exists(csv_file):
        print(f"❌ Sample data file '{csv_file}' not found!")
        print("Please ensure the CSV file exists in the current directory.")
        return
    
    print("🎬 MOCAP Converter - Example Usage\n")
    
    examples = [
        {
            "name": "Quick Preview",
            "description": "Fast preview with reduced frames for testing",
            "args": [csv_file, "--output", "preview.py", "--frame-step", "10", "--chunk-size", "25"]
        },
        {
            "name": "High Performance", 
            "description": "Optimized for speed with larger chunks",
            "args": [csv_file, "--output", "performance.py", "--chunk-size", "100", "--frame-step", "2"]
        },
        {
            "name": "JSON Export",
            "description": "Lightweight JSON format for memory efficiency", 
            "args": [csv_file, "--json-only", "--frame-step", "5"]
        },
        {
            "name": "Full Quality",
            "description": "Maximum quality with all frames",
            "args": [csv_file, "--output", "full_quality.py", "--chunk-size", "75"]
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"🔹 Example {i}: {example['name']}")
        print(f"   {example['description']}")
        print(f"   Command: python mocap_converter.py {' '.join(example['args'])}")
        
        # Actually run the example
        original_argv = sys.argv[:]
        try:
            sys.argv = ["mocap_converter.py"] + example['args'] + ["--quiet"]
            converter_main()
            print("   ✅ Generated successfully!\n")
        except Exception as e:
            print(f"   ❌ Error: {e}\n")
        finally:
            sys.argv = original_argv
    
    print("📋 Generated Files:")
    for filename in os.listdir("."):
        if filename.endswith(('.py', '.json')) and filename not in ['example_usage.py', 'mocap_converter.py', 'blender_script_generator.py', 'DIZIONARIO.py']:
            size = os.path.getsize(filename)
            size_str = f"{size/1024:.1f}KB" if size < 1024*1024 else f"{size/(1024*1024):.1f}MB"
            print(f"   📄 {filename} ({size_str})")
    
    print("\n🚀 Tips:")
    print("   • Use --frame-step 5-10 for quick previews")
    print("   • Use --chunk-size 100+ for better performance") 
    print("   • Use --json-only for very large datasets")
    print("   • Check README.md for detailed documentation")

if __name__ == "__main__":
    run_example()