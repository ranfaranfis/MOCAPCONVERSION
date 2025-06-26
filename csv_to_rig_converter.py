#!/usr/bin/env python3
"""
CSV to Rig Animation Converter

A complete Python tool that converts CSV blendshape data to FaceIt rig animations.
This tool is completely autonomous with all conversions hardcoded.

Usage:
    python csv_to_rig_converter.py input.csv [--output output.py] [--format blender|json]
"""

import csv
import json
import math
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass


@dataclass
class Transform:
    """Represents a bone transformation."""
    location: List[float]
    rotation_quaternion: List[float]
    rotation_euler: List[float]
    scale: List[float]


@dataclass
class FrameData:
    """Represents animation data for a single frame."""
    frame_number: int
    timecode: str
    transforms: Dict[str, Transform]


class CSVToRigConverter:
    """
    Main converter class that handles CSV parsing and rig animation generation.
    All mappings and conversion values are hardcoded for autonomous operation.
    """
    
    def __init__(self):
        self.bone_mappings = self._get_bone_mappings()
        self.conversion_data = self._get_conversion_data()
        self.frame_data: List[FrameData] = []
        
    def _get_bone_mappings(self) -> Dict[str, Dict[str, str]]:
        """Returns hardcoded bone mappings from blendshapes to rig controls."""
        return {
            # Face Cap blendshapes - using capitalized names to match CSV
            "EyeBlinkLeft": {
                "bone": "c_eyelid_upper.L",
                "object": "FaceitControlRig",
                "transform_type": "LOC_Y",
                "source": "face_cap"
            },
            "EyeBlinkRight": {
                "bone": "c_eyelid_upper.R",
                "object": "FaceitControlRig",
                "transform_type": "LOC_Y",
                "source": "face_cap"
            },
            "EyeSquintLeft": {
                "bone": "c_eyelid_lower.L",
                "object": "FaceitControlRig",
                "transform_type": "LOC_Y",
                "source": "face_cap"
            },
            "EyeSquintRight": {
                "bone": "c_eyelid_lower.R",
                "object": "FaceitControlRig",
                "transform_type": "LOC_Y",
                "source": "face_cap"
            },
            "EyeWideLeft": {
                "bone": "c_eyelid_upper.L",
                "object": "FaceitControlRig",
                "transform_type": "LOC_Y",
                "source": "face_cap"
            },
            "EyeWideRight": {
                "bone": "c_eyelid_upper.R",
                "object": "FaceitControlRig",
                "transform_type": "LOC_Y",
                "source": "face_cap"
            },
            "EyeLookUpLeft": {
                "bone": "c_lookat_mch.L",
                "object": "FaceitControlRig",
                "transform_type": "ROT_X",
                "source": "face_cap"
            },
            "EyeLookUpRight": {
                "bone": "c_lookat_mch.R",
                "object": "FaceitControlRig",
                "transform_type": "ROT_X",
                "source": "face_cap"
            },
            "EyeLookDownLeft": {
                "bone": "c_lookat_mch.L",
                "object": "FaceitControlRig",
                "transform_type": "ROT_X",
                "source": "face_cap"
            },
            "EyeLookDownRight": {
                "bone": "c_lookat_mch.R",
                "object": "FaceitControlRig",
                "transform_type": "ROT_X",
                "source": "face_cap"
            },
            "EyeLookInLeft": {
                "bone": "c_lookat_mch.L",
                "object": "FaceitControlRig",
                "transform_type": "ROT_Z",
                "source": "face_cap"
            },
            "EyeLookInRight": {
                "bone": "c_lookat_mch.R",
                "object": "FaceitControlRig",
                "transform_type": "ROT_Z",
                "source": "face_cap"
            },
            "EyeLookOutLeft": {
                "bone": "c_lookat_mch.L",
                "object": "FaceitControlRig",
                "transform_type": "ROT_Z",
                "source": "face_cap"
            },
            "EyeLookOutRight": {
                "bone": "c_lookat_mch.R",
                "object": "FaceitControlRig",
                "transform_type": "ROT_Z",
                "source": "face_cap"
            },
            "MouthClose": {
                "bone": "c_mouth_close",
                "object": "FaceitControlRig",
                "transform_type": "LOC_Z",
                "source": "face_cap"
            },
            "MouthFunnel": {
                "bone": "c_mouth_funnel",
                "object": "FaceitControlRig",
                "transform_type": "LOC_Z",
                "source": "face_cap"
            },
            "MouthPucker": {
                "bone": "c_mouth_pucker",
                "object": "FaceitControlRig",
                "transform_type": "LOC_Z",
                "source": "face_cap"
            },
            "MouthSmileLeft": {
                "bone": "c_mouth_smile.L",
                "object": "FaceitControlRig",
                "transform_type": "ROT_Z",
                "source": "face_cap"
            },
            "MouthSmileRight": {
                "bone": "c_mouth_smile.R",
                "object": "FaceitControlRig",
                "transform_type": "ROT_Z",
                "source": "face_cap"
            },
            "MouthFrownLeft": {
                "bone": "c_mouth_frown.L",
                "object": "FaceitControlRig",
                "transform_type": "ROT_Z",
                "source": "face_cap"
            },
            "MouthFrownRight": {
                "bone": "c_mouth_frown.R",
                "object": "FaceitControlRig",
                "transform_type": "ROT_Z",
                "source": "face_cap"
            },
            "JawOpen": {
                "bone": "c_jaw_target",
                "object": "FaceitControlRig",
                "transform_type": "LOC_Y",
                "source": "face_cap"
            },
            "JawRight": {
                "bone": "c_jaw_target",
                "object": "FaceitControlRig",
                "transform_type": "LOC_X",
                "source": "face_cap"
            },
            "JawLeft": {
                "bone": "c_jaw_target",
                "object": "FaceitControlRig",
                "transform_type": "LOC_X",
                "source": "face_cap"
            },
            "JawForward": {
                "bone": "c_jaw_target",
                "object": "FaceitControlRig",
                "transform_type": "LOC_Z",
                "source": "face_cap"
            },
            "TongueOut": {
                "bone": "c_tongue",
                "object": "FaceitControlRig",
                "transform_type": "LOC_Y",
                "source": "face_cap"
            },
            # Additional blendshapes with special controls
            "MouthStretchLeft": {
                "bone": "c_lips_corner_adjust.L",
                "object": "FaceitControlRig",
                "transform_type": "LOC_Y",
                "source": "face_cap"
            },
            "MouthStretchRight": {
                "bone": "c_lips_corner_adjust.R",
                "object": "FaceitControlRig",
                "transform_type": "LOC_Y",
                "source": "face_cap"
            },
            # Additional mouth controls found in CSV
            "MouthRight": {
                "bone": "c_jaw_target",
                "object": "FaceitControlRig",
                "transform_type": "LOC_X",
                "source": "face_cap"
            },
            "MouthLeft": {
                "bone": "c_jaw_target",
                "object": "FaceitControlRig",
                "transform_type": "LOC_X",
                "source": "face_cap"
            },
            "MouthDimpleLeft": {
                "bone": "c_mouth_smile.L",
                "object": "FaceitControlRig",
                "transform_type": "ROT_Z",
                "source": "face_cap"
            },
            "MouthDimpleRight": {
                "bone": "c_mouth_smile.R",
                "object": "FaceitControlRig",
                "transform_type": "ROT_Z",
                "source": "face_cap"
            },
            "MouthRollLower": {
                "bone": "c_lips_lower",
                "object": "FaceitControlRig",
                "transform_type": "ROT_Z",
                "source": "face_cap"
            },
            "MouthRollUpper": {
                "bone": "c_lips_upper",
                "object": "FaceitControlRig",
                "transform_type": "ROT_Z",
                "source": "face_cap"
            },
            "MouthShrugLower": {
                "bone": "c_lips_lower",
                "object": "FaceitControlRig",
                "transform_type": "LOC_Y",
                "source": "face_cap"
            },
            "MouthShrugUpper": {
                "bone": "c_lips_upper",
                "object": "FaceitControlRig",
                "transform_type": "LOC_Y",
                "source": "face_cap"
            },
            "MouthPressLeft": {
                "bone": "c_lips_corner.L",
                "object": "FaceitControlRig",
                "transform_type": "LOC_Z",
                "source": "face_cap"
            },
            "MouthPressRight": {
                "bone": "c_lips_corner.R",
                "object": "FaceitControlRig",
                "transform_type": "LOC_Z",
                "source": "face_cap"
            },
            "BrowDownLeft": {
                "bone": "c_brow_lower.L",
                "object": "FaceitControlRig",
                "transform_type": "LOC_Y",
                "source": "face_cap"
            },
            "BrowDownRight": {
                "bone": "c_brow_lower.R",
                "object": "FaceitControlRig",
                "transform_type": "LOC_Y",
                "source": "face_cap"
            },
            "BrowInnerUp": {
                "bone": "c_brow_inner",
                "object": "FaceitControlRig",
                "transform_type": "LOC_Y",
                "source": "face_cap"
            },
            "BrowOuterUpLeft": {
                "bone": "c_brow_outer.L",
                "object": "FaceitControlRig",
                "transform_type": "LOC_Y",
                "source": "face_cap"
            },
            "BrowOuterUpRight": {
                "bone": "c_brow_outer.R",
                "object": "FaceitControlRig",
                "transform_type": "LOC_Y",
                "source": "face_cap"
            },
            "CheekPuff": {
                "bone": "c_cheek.L",
                "object": "FaceitControlRig",
                "transform_type": "LOC_Z",
                "source": "face_cap"
            },
            "CheekSquintLeft": {
                "bone": "c_cheek.L",
                "object": "FaceitControlRig",
                "transform_type": "LOC_Y",
                "source": "face_cap"
            },
            "CheekSquintRight": {
                "bone": "c_cheek.R",
                "object": "FaceitControlRig",
                "transform_type": "LOC_Y",
                "source": "face_cap"
            },
            "NoseSneerLeft": {
                "bone": "c_nose.L",
                "object": "FaceitControlRig",
                "transform_type": "ROT_Z",
                "source": "face_cap"
            },
            "NoseSneerRight": {
                "bone": "c_nose.R",
                "object": "FaceitControlRig",
                "transform_type": "ROT_Z",
                "source": "face_cap"
            }
        }
    
    def _get_conversion_data(self) -> Dict[str, Any]:
        """Returns hardcoded conversion values and scaling factors."""
        return {
            "scaling_factors": {
                "LOC_X": 0.1,
                "LOC_Y": 2.0,
                "LOC_Z": 1.0,
                "ROT_X": 0.5,
                "ROT_Y": 0.5,
                "ROT_Z": 0.3,
            },
            "default_transform": {
                "location": [0.0, 0.0, 0.0],
                "rotation_quaternion": [1.0, 0.0, 0.0, 0.0],
                "rotation_euler": [0.0, 0.0, 0.0],
                "scale": [1.0, 1.0, 1.0]
            },
            "frame_rate": 30.0,
            "bone_limits": {
                "min_location": -10.0,
                "max_location": 10.0,
                "min_rotation": -math.pi,
                "max_rotation": math.pi
            }
        }
    
    def parse_timecode(self, timecode: str) -> int:
        """Convert timecode to frame number."""
        try:
            # Format: HH:MM:SS:FF.fff
            parts = timecode.split(':')
            if len(parts) == 4:
                hours = int(parts[0])
                minutes = int(parts[1]) 
                seconds = int(parts[2])
                frame_part = parts[3].split('.')[0]
                frames = int(frame_part)
                
                total_frames = (hours * 3600 + minutes * 60 + seconds) * int(self.conversion_data["frame_rate"]) + frames
                return total_frames
            else:
                return 1
        except:
            return 1
    
    def apply_blendshape_to_transform(self, blendshape_name: str, value: float, bone_name: str, 
                                    current_transform: Transform) -> Transform:
        """Apply blendshape value to bone transform based on mappings."""
        if blendshape_name not in self.bone_mappings:
            return current_transform
            
        mapping = self.bone_mappings[blendshape_name]
        transform_type = mapping["transform_type"]
        scaling_factor = self.conversion_data["scaling_factors"].get(transform_type, 1.0)
        
        # Apply scaling and clamping
        scaled_value = value * scaling_factor
        
        # Create new transform
        new_transform = Transform(
            location=current_transform.location.copy(),
            rotation_quaternion=current_transform.rotation_quaternion.copy(),
            rotation_euler=current_transform.rotation_euler.copy(),
            scale=current_transform.scale.copy()
        )
        
        # Apply transformation based on type
        if transform_type == "LOC_X":
            new_transform.location[0] += scaled_value
        elif transform_type == "LOC_Y":
            new_transform.location[1] += scaled_value
        elif transform_type == "LOC_Z":
            new_transform.location[2] += scaled_value
        elif transform_type == "ROT_X":
            new_transform.rotation_euler[0] += scaled_value
        elif transform_type == "ROT_Y":
            new_transform.rotation_euler[1] += scaled_value
        elif transform_type == "ROT_Z":
            new_transform.rotation_euler[2] += scaled_value
            
        # Apply limits
        limits = self.conversion_data["bone_limits"]
        for i in range(3):
            new_transform.location[i] = max(limits["min_location"], 
                                          min(limits["max_location"], new_transform.location[i]))
            new_transform.rotation_euler[i] = max(limits["min_rotation"],
                                                min(limits["max_rotation"], new_transform.rotation_euler[i]))
        
        return new_transform
    
    def parse_csv(self, csv_file_path: str) -> bool:
        """Parse CSV file and convert to frame data."""
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row_idx, row in enumerate(reader):
                    frame_number = self.parse_timecode(row.get('Timecode', f'00:00:00:{row_idx:02d}.000'))
                    timecode = row.get('Timecode', f'00:00:00:{row_idx:02d}.000')
                    
                    # Initialize transforms for all bones
                    frame_transforms = {}
                    
                    # Get all unique bones from mappings
                    unique_bones = set()
                    for mapping in self.bone_mappings.values():
                        unique_bones.add(mapping["bone"])
                    
                    # Initialize each bone with default transform
                    for bone_name in unique_bones:
                        default = self.conversion_data["default_transform"]
                        frame_transforms[bone_name] = Transform(
                            location=default["location"].copy(),
                            rotation_quaternion=default["rotation_quaternion"].copy(),
                            rotation_euler=default["rotation_euler"].copy(),
                            scale=default["scale"].copy()
                        )
                    
                    # Apply blendshape values to transforms
                    for blendshape_name, value_str in row.items():
                        if blendshape_name in ['Timecode', 'BlendShapeCount']:
                            continue
                            
                        try:
                            value = float(value_str)
                            if blendshape_name in self.bone_mappings:
                                bone_name = self.bone_mappings[blendshape_name]["bone"]
                                if bone_name in frame_transforms:
                                    frame_transforms[bone_name] = self.apply_blendshape_to_transform(
                                        blendshape_name, value, bone_name, frame_transforms[bone_name]
                                    )
                        except ValueError:
                            continue
                    
                    # Create frame data
                    frame_data = FrameData(
                        frame_number=frame_number,
                        timecode=timecode,
                        transforms=frame_transforms
                    )
                    
                    self.frame_data.append(frame_data)
                    
            print(f"Successfully parsed {len(self.frame_data)} frames from CSV")
            return True
            
        except Exception as e:
            print(f"Error parsing CSV file: {e}")
            return False
    
    def export_to_blender_script(self, output_path: str) -> bool:
        """Export animation data as Blender Python script."""
        try:
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write('import bpy\n')
                file.write('from mathutils import Vector, Euler, Quaternion\n\n')
                file.write('# CSV to Rig Animation - Generated Script\n')
                file.write('# Apply FaceIt rig animation from CSV blendshape data\n\n')
                file.write('def apply_faceit_animation():\n')
                file.write('    """Apply animation to FaceIt rig."""\n')
                file.write('    \n')
                file.write('    # Get the armature object\n')
                file.write('    armature = bpy.data.objects.get("FaceitControlRig")\n')
                file.write('    if not armature:\n')
                file.write('        print("FaceitControlRig not found!")\n')
                file.write('        return\n')
                file.write('    \n')
                file.write('    # Set to pose mode\n')
                file.write('    bpy.context.view_layer.objects.active = armature\n')
                file.write('    bpy.ops.object.mode_set(mode="POSE")\n')
                file.write('    \n')
                file.write('    # Clear existing keyframes\n')
                file.write('    armature.animation_data_clear()\n')
                file.write('    \n')
                file.write('    # Animation data\n')
                
                for frame in self.frame_data:
                    file.write(f'    \n    # Frame {frame.frame_number}\n')
                    file.write(f'    bpy.context.scene.frame_set({frame.frame_number})\n')
                    
                    for bone_name, transform in frame.transforms.items():
                        file.write(f'    \n    # Bone: {bone_name}\n')
                        file.write(f'    if "{bone_name}" in armature.pose.bones:\n')
                        file.write(f'        bone = armature.pose.bones["{bone_name}"]\n')
                        file.write(f'        bone.location = Vector({transform.location})\n')
                        file.write(f'        bone.rotation_euler = Euler({transform.rotation_euler})\n')
                        file.write(f'        bone.scale = Vector({transform.scale})\n')
                        file.write(f'        bone.keyframe_insert(data_path="location")\n')
                        file.write(f'        bone.keyframe_insert(data_path="rotation_euler")\n')
                        file.write(f'        bone.keyframe_insert(data_path="scale")\n')
                
                file.write('\n    print("Animation applied successfully!")\n\n')
                file.write('if __name__ == "__main__":\n')
                file.write('    apply_faceit_animation()\n')
                
            print(f"Blender script exported to: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error exporting Blender script: {e}")
            return False
    
    def export_to_json(self, output_path: str) -> bool:
        """Export animation data as JSON."""
        try:
            animation_data = {
                "metadata": {
                    "frame_count": len(self.frame_data),
                    "frame_rate": self.conversion_data["frame_rate"],
                    "source": "CSV to Rig Converter",
                    "rig_type": "FaceIt"
                },
                "frames": {}
            }
            
            for frame in self.frame_data:
                frame_key = str(frame.frame_number)
                animation_data["frames"][frame_key] = {
                    "timecode": frame.timecode,
                    "bones": {}
                }
                
                for bone_name, transform in frame.transforms.items():
                    animation_data["frames"][frame_key]["bones"][bone_name] = {
                        "location": transform.location,
                        "rotation_quaternion": transform.rotation_quaternion,
                        "rotation_euler": transform.rotation_euler,
                        "scale": transform.scale
                    }
            
            with open(output_path, 'w', encoding='utf-8') as file:
                json.dump(animation_data, file, indent=2, ensure_ascii=False)
                
            print(f"JSON animation data exported to: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error exporting JSON: {e}")
            return False
    
    def convert(self, csv_file_path: str, output_path: str, output_format: str = "blender") -> bool:
        """Main conversion method."""
        print(f"Converting {csv_file_path} to {output_format} format...")
        
        # Parse CSV
        if not self.parse_csv(csv_file_path):
            return False
        
        # Export based on format
        if output_format.lower() == "blender":
            return self.export_to_blender_script(output_path)
        elif output_format.lower() == "json":
            return self.export_to_json(output_path)
        else:
            print(f"Unsupported output format: {output_format}")
            return False
    
    def get_summary(self) -> Dict[str, Any]:
        """Get conversion summary information."""
        return {
            "total_frames": len(self.frame_data),
            "total_bones": len(set(mapping["bone"] for mapping in self.bone_mappings.values())),
            "total_blendshapes": len(self.bone_mappings),
            "frame_rate": self.conversion_data["frame_rate"],
            "supported_blendshapes": list(self.bone_mappings.keys())
        }


def main():
    """Command line interface."""
    parser = argparse.ArgumentParser(description='Convert CSV blendshape data to FaceIt rig animation')
    parser.add_argument('input_csv', help='Input CSV file with blendshape data')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--format', '-f', choices=['blender', 'json'], default='blender',
                       help='Output format (default: blender)')
    parser.add_argument('--summary', '-s', action='store_true',
                       help='Show conversion summary')
    
    args = parser.parse_args()
    
    # Validate input file
    input_path = Path(args.input_csv)
    if not input_path.exists():
        print(f"Error: Input file '{args.input_csv}' not found")
        sys.exit(1)
    
    # Generate output path if not provided
    if args.output:
        output_path = args.output
    else:
        if args.format == 'blender':
            output_path = input_path.with_suffix('.py')
        else:
            output_path = input_path.with_suffix('.json')
    
    # Create converter and run conversion
    converter = CSVToRigConverter()
    
    # Show summary if requested
    if args.summary:
        summary = converter.get_summary()
        print("\nConverter Summary:")
        print(f"- Supported blendshapes: {summary['total_blendshapes']}")
        print(f"- Target bones: {summary['total_bones']}")
        print(f"- Frame rate: {summary['frame_rate']} FPS")
        print("\nSupported blendshapes:")
        for blendshape in summary['supported_blendshapes']:
            print(f"  - {blendshape}")
        print()
    
    # Run conversion
    success = converter.convert(args.input_csv, str(output_path), args.format)
    
    if success:
        print(f"\nConversion completed successfully!")
        print(f"Output: {output_path}")
        
        # Show final summary
        summary = converter.get_summary()
        print(f"\nProcessed {summary['total_frames']} frames")
        print(f"Applied to {summary['total_bones']} bones")
    else:
        print("\nConversion failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()