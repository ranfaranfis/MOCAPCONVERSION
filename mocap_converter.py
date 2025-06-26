#!/usr/bin/env python3
"""
MOCAP to Blender Conversion Tool - Enhanced Performance Version

This script provides an easy-to-use interface for converting mocap CSV data
to optimized Blender scripts. It includes various optimization techniques to
prevent crashes and improve performance.

Usage examples:
    # Generate optimized script with default settings
    python mocap_converter.py data.csv
    
    # Generate with custom settings
    python mocap_converter.py data.csv --output my_animation.py --frame-step 2 --chunk-size 100
    
    # Export to JSON format only (lightweight)
    python mocap_converter.py data.csv --json-only --frame-step 5
    
    # Generate both Python and JSON versions
    python mocap_converter.py data.csv --json --frame-step 1
"""

import os
import sys
import argparse
from blender_script_generator import BlenderScriptGenerator

def main():
    """Main function with enhanced command-line interface."""
    parser = argparse.ArgumentParser(
        description='Convert mocap CSV data to optimized Blender scripts',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Performance Guidelines:
    --chunk-size: Larger values use more memory but can be faster (default: 50)
    --frame-step: Use higher values for testing or lower FPS (default: 1)
    
Optimization Features:
    • Batch keyframe insertion instead of individual calls
    • Progress feedback during execution
    • Memory optimization with chunk processing
    • Error handling with try/catch blocks
    • Frame sampling for reduced data load
    • JSON export for lightweight imports
    
Example workflows:
    # Quick test with reduced frames
    python mocap_converter.py data.csv --frame-step 10 --output test.py
    
    # Full quality animation
    python mocap_converter.py data.csv --chunk-size 100
    
    # Lightweight JSON export
    python mocap_converter.py data.csv --json-only --frame-step 2
        """
    )
    
    parser.add_argument('csv_file', help='Path to CSV mocap data file')
    parser.add_argument('--output', '-o', default='mocap_animation.py', 
                       help='Output script filename (default: mocap_animation.py)')
    parser.add_argument('--chunk-size', '-c', type=int, default=50,
                       help='Chunk size for processing frames (default: 50, larger=faster but more memory)')
    parser.add_argument('--frame-step', '-s', type=int, default=1,
                       help='Frame sampling step (default: 1, higher=fewer frames)')
    parser.add_argument('--start-frame', '-f', type=int, default=1,
                       help='Starting frame number in Blender (default: 1)')
    parser.add_argument('--json', action='store_true',
                       help='Also export to JSON format (creates JSON + importer script)')
    parser.add_argument('--json-only', action='store_true',
                       help='Only export to JSON format (no Python script)')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Reduce output verbosity')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not os.path.exists(args.csv_file):
        print(f"Error: CSV file '{args.csv_file}' not found")
        return 1
    
    if args.chunk_size < 1:
        print("Error: chunk-size must be at least 1")
        return 1
        
    if args.frame_step < 1:
        print("Error: frame-step must be at least 1")
        return 1
    
    try:
        if not args.quiet:
            print(f"🎬 MOCAP to Blender Converter - Enhanced Performance")
            print(f"📁 Input file: {args.csv_file}")
            print(f"⚙️  Settings: chunk-size={args.chunk_size}, frame-step={args.frame_step}")
            print()
        
        generator = BlenderScriptGenerator(args.csv_file)
        
        if args.json_only:
            if not args.quiet:
                print("📄 Generating JSON export only...")
            json_file = generator.export_to_json(
                output_file="mocap_data.json", 
                frame_step=args.frame_step
            )
            importer_file = generator.generate_json_importer_script(json_file)
            
            if not args.quiet:
                print(f"✅ Generated JSON files:")
                print(f"   📊 Data: {json_file}")
                print(f"   🐍 Importer: {importer_file}")
                
        else:
            if not args.quiet:
                print("🐍 Generating optimized Python script...")
            script_file = generator.generate_optimized_script(
                output_file=args.output,
                chunk_size=args.chunk_size,
                frame_step=args.frame_step,
                start_frame=args.start_frame
            )
            
            if not args.quiet:
                print(f"✅ Generated optimized script: {script_file}")
            
            if args.json:
                if not args.quiet:
                    print("📄 Also generating JSON export...")
                json_file = generator.export_to_json(frame_step=args.frame_step)
                importer_file = generator.generate_json_importer_script(json_file)
                
                if not args.quiet:
                    print(f"✅ Generated JSON files:")
                    print(f"   📊 Data: {json_file}")
                    print(f"   🐍 Importer: {importer_file}")
        
        if not args.quiet:
            print()
            print("🚀 Performance Optimizations Applied:")
            print("   • Batch keyframe insertion (reduces individual API calls)")
            print("   • Chunk-based processing (optimizes memory usage)")
            print("   • Progress feedback (shows import status)")
            print("   • Error handling (prevents crashes)")
            print("   • Frame sampling (reduces data when needed)")
            print()
            print("📋 Usage in Blender:")
            if not args.json_only:
                print(f"   1. Open Blender with your rigged character")
                print(f"   2. Go to Scripting workspace")
                print(f"   3. Open and run: {args.output}")
            if args.json or args.json_only:
                print(f"   Alternative: Run json_importer.py for lighter import")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if not args.quiet:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())