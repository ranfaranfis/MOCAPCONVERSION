#!/usr/bin/env python3
"""
Animation Data Inspector

A utility script to inspect and validate generated animation data.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any


def analyze_animation_data(json_file: str) -> Dict[str, Any]:
    """Analyze animation data from JSON file."""
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        metadata = data.get("metadata", {})
        frames = data.get("frames", {})
        
        # Collect statistics
        stats = {
            "total_frames": len(frames),
            "frame_rate": metadata.get("frame_rate", "Unknown"),
            "source": metadata.get("source", "Unknown"),
            "rig_type": metadata.get("rig_type", "Unknown"),
            "bones": set(),
            "active_bones": set(),
            "bone_activity": {},
            "transform_ranges": {
                "location": {"min": [float('inf')] * 3, "max": [float('-inf')] * 3},
                "rotation": {"min": [float('inf')] * 3, "max": [float('-inf')] * 3}
            }
        }
        
        # Analyze each frame
        for frame_num, frame_data in frames.items():
            bones_data = frame_data.get("bones", {})
            
            for bone_name, transform in bones_data.items():
                stats["bones"].add(bone_name)
                
                # Check if bone has non-default values
                location = transform.get("location", [0, 0, 0])
                rotation = transform.get("rotation_euler", [0, 0, 0])
                
                is_active = (
                    any(abs(v) > 0.001 for v in location) or
                    any(abs(v) > 0.001 for v in rotation)
                )
                
                if is_active:
                    stats["active_bones"].add(bone_name)
                    stats["bone_activity"][bone_name] = stats["bone_activity"].get(bone_name, 0) + 1
                
                # Update ranges
                for i in range(3):
                    if location[i] < stats["transform_ranges"]["location"]["min"][i]:
                        stats["transform_ranges"]["location"]["min"][i] = location[i]
                    if location[i] > stats["transform_ranges"]["location"]["max"][i]:
                        stats["transform_ranges"]["location"]["max"][i] = location[i]
                    
                    if rotation[i] < stats["transform_ranges"]["rotation"]["min"][i]:
                        stats["transform_ranges"]["rotation"]["min"][i] = rotation[i]
                    if rotation[i] > stats["transform_ranges"]["rotation"]["max"][i]:
                        stats["transform_ranges"]["rotation"]["max"][i] = rotation[i]
        
        return stats
        
    except Exception as e:
        print(f"Error analyzing animation data: {e}")
        return {}


def print_analysis_report(stats: Dict[str, Any]):
    """Print detailed analysis report."""
    print("=== Animation Data Analysis Report ===\n")
    
    print(f"Source: {stats.get('source', 'Unknown')}")
    print(f"Rig Type: {stats.get('rig_type', 'Unknown')}")
    print(f"Frame Rate: {stats.get('frame_rate', 'Unknown')} FPS")
    print(f"Total Frames: {stats.get('total_frames', 0)}")
    print(f"Duration: {stats.get('total_frames', 0) / stats.get('frame_rate', 30):.2f} seconds")
    print()
    
    print(f"Total Bones: {len(stats.get('bones', set()))}")
    print(f"Active Bones: {len(stats.get('active_bones', set()))}")
    print()
    
    print("Active Bones (with movement):")
    bone_activity = stats.get('bone_activity', {})
    for bone in sorted(stats.get('active_bones', set())):
        activity_percent = (bone_activity.get(bone, 0) / stats.get('total_frames', 1)) * 100
        print(f"  - {bone}: active in {bone_activity.get(bone, 0)} frames ({activity_percent:.1f}%)")
    print()
    
    print("Transform Ranges:")
    ranges = stats.get('transform_ranges', {})
    loc_min = ranges.get('location', {}).get('min', [0, 0, 0])
    loc_max = ranges.get('location', {}).get('max', [0, 0, 0])
    rot_min = ranges.get('rotation', {}).get('min', [0, 0, 0])
    rot_max = ranges.get('rotation', {}).get('max', [0, 0, 0])
    
    print(f"  Location X: {loc_min[0]:.3f} to {loc_max[0]:.3f}")
    print(f"  Location Y: {loc_min[1]:.3f} to {loc_max[1]:.3f}")
    print(f"  Location Z: {loc_min[2]:.3f} to {loc_max[2]:.3f}")
    print(f"  Rotation X: {rot_min[0]:.3f} to {rot_max[0]:.3f}")
    print(f"  Rotation Y: {rot_min[1]:.3f} to {rot_max[1]:.3f}")
    print(f"  Rotation Z: {rot_min[2]:.3f} to {rot_max[2]:.3f}")
    print()
    
    print("Inactive Bones (no movement):")
    inactive_bones = stats.get('bones', set()) - stats.get('active_bones', set())
    for bone in sorted(inactive_bones):
        print(f"  - {bone}")


def main():
    """Command line interface."""
    if len(sys.argv) != 2:
        print("Usage: python animation_inspector.py <animation.json>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    
    if not Path(json_file).exists():
        print(f"Error: File '{json_file}' not found")
        sys.exit(1)
    
    stats = analyze_animation_data(json_file)
    
    if stats:
        print_analysis_report(stats)
    else:
        print("Failed to analyze animation data")
        sys.exit(1)


if __name__ == "__main__":
    main()