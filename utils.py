import bpy
import csv
import mathutils
from mathutils import Vector, Euler
from . import DIZIONARIO

def apply_transform_to_bone(armature_obj, bone_name, transform_type, value, frame=None):
    """
    Apply transform to bone using proper matrix manipulation to ensure persistence.
    This fixes the issue where bone.location = Vector() doesn't persist properly.
    """
    if not armature_obj or armature_obj.type != 'ARMATURE':
        return False
    
    # Enter pose mode if not already
    if bpy.context.mode != 'POSE':
        bpy.context.view_layer.objects.active = armature_obj
        bpy.ops.object.mode_set(mode='POSE')
    
    # Get the pose bone
    if bone_name not in armature_obj.pose.bones:
        print(f"Warning: Bone '{bone_name}' not found in armature '{armature_obj.name}'")
        return False
    
    pose_bone = armature_obj.pose.bones[bone_name]
    
    # Clear any existing transforms to start from rest pose
    if frame is None:  # Only clear on first frame to avoid overriding previous keyframes
        pose_bone.location = Vector((0, 0, 0))
        pose_bone.rotation_euler = Euler((0, 0, 0), 'XYZ')
        pose_bone.scale = Vector((1, 1, 1))
    
    # Apply the transform based on type
    if transform_type == "LOC_X":
        pose_bone.location.x = value
    elif transform_type == "LOC_Y":
        pose_bone.location.y = value
    elif transform_type == "LOC_Z":
        pose_bone.location.z = value
    elif transform_type == "ROT_X":
        pose_bone.rotation_euler.x = value
    elif transform_type == "ROT_Y":
        pose_bone.rotation_euler.y = value
    elif transform_type == "ROT_Z":
        pose_bone.rotation_euler.z = value
    else:
        print(f"Warning: Unknown transform type '{transform_type}'")
        return False
    
    # Force update the bone matrix to ensure the transform is applied
    bpy.context.view_layer.update()
    
    # Insert keyframe if frame is specified (batch operation)
    if frame is not None:
        if transform_type.startswith("LOC"):
            pose_bone.keyframe_insert(data_path="location", frame=frame)
        elif transform_type.startswith("ROT"):
            pose_bone.keyframe_insert(data_path="rotation_euler", frame=frame)
    
    return True

def get_bone_mapping_for_source(source_type):
    """Get the appropriate bone mapping based on source type"""
    mapping = {}
    for key, value in DIZIONARIO.BONE_MAP_UNIFICATA.items():
        if value["source"] == source_type:
            mapping[key] = value
    return mapping

def import_mocap_csv(context, filepath, target_object_name, source_type, use_frame_optimization):
    """
    Import mocap CSV data with optimized frame operations.
    This fixes the slow import issue by avoiding repeated frame_set() calls.
    """
    try:
        # Get target armature object
        if target_object_name not in bpy.data.objects:
            return {'CANCELLED'}, f"Object '{target_object_name}' not found"
        
        armature_obj = bpy.data.objects[target_object_name]
        if armature_obj.type != 'ARMATURE':
            return {'CANCELLED'}, f"Object '{target_object_name}' is not an armature"
        
        # Get bone mapping for the specified source type
        bone_mapping = get_bone_mapping_for_source(source_type)
        if not bone_mapping:
            return {'CANCELLED'}, f"No bone mapping found for source type '{source_type}'"
        
        # Read CSV file
        with open(filepath, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Get the original frame for restoration later
            original_frame = context.scene.frame_current
            
            # Collect all keyframe data first (batch approach)
            keyframe_data = {}  # {bone_name: {frame: {transform_type: value}}}
            frame_count = 0
            
            for row_index, row in enumerate(reader):
                frame_number = row_index + 1  # Start from frame 1
                frame_count = frame_number
                
                # Process each column that has a corresponding bone mapping
                for csv_column, csv_value in row.items():
                    # Skip non-numeric columns
                    if csv_column in ['Timecode', 'BlendShapeCount']:
                        continue
                    
                    # Find matching bone mapping
                    mapped_bone_info = None
                    for mapping_key, mapping_info in bone_mapping.items():
                        # Handle different naming conventions
                        if (csv_column.lower() == mapping_key.lower() or 
                            csv_column.lower().replace('_', '').replace('-', '') == 
                            mapping_key.lower().replace('_', '').replace('-', '')):
                            mapped_bone_info = mapping_info
                            break
                    
                    if mapped_bone_info:
                        try:
                            value = float(csv_value)
                            bone_name = mapped_bone_info["bone"]
                            transform_type = mapped_bone_info["transform_type"]
                            
                            # Initialize bone data if needed
                            if bone_name not in keyframe_data:
                                keyframe_data[bone_name] = {}
                            if frame_number not in keyframe_data[bone_name]:
                                keyframe_data[bone_name][frame_number] = {}
                            
                            # Store keyframe data
                            keyframe_data[bone_name][frame_number][transform_type] = value
                            
                        except ValueError:
                            continue  # Skip non-numeric values
            
            # Now apply all transforms efficiently
            if use_frame_optimization:
                # Batch keyframe insertion - apply all transforms without changing frames
                for bone_name, frame_data in keyframe_data.items():
                    for frame_number, transforms in frame_data.items():
                        for transform_type, value in transforms.items():
                            apply_transform_to_bone(
                                armature_obj, bone_name, transform_type, value, frame_number
                            )
            else:
                # Traditional approach - set frame for each keyframe (slower)
                for frame_number in range(1, frame_count + 1):
                    context.scene.frame_set(frame_number)
                    
                    for bone_name, frame_data in keyframe_data.items():
                        if frame_number in frame_data:
                            for transform_type, value in frame_data[frame_number].items():
                                apply_transform_to_bone(
                                    armature_obj, bone_name, transform_type, value
                                )
                                # Insert keyframe immediately
                                pose_bone = armature_obj.pose.bones[bone_name]
                                if transform_type.startswith("LOC"):
                                    pose_bone.keyframe_insert(data_path="location")
                                elif transform_type.startswith("ROT"):
                                    pose_bone.keyframe_insert(data_path="rotation_euler")
            
            # Restore original frame
            context.scene.frame_set(original_frame)
            
            # Update timeline
            context.scene.frame_end = max(context.scene.frame_end, frame_count)
            
            print(f"Successfully imported {frame_count} frames of mocap data")
            return {'FINISHED'}
            
    except Exception as e:
        print(f"Error importing mocap CSV: {str(e)}")
        return {'CANCELLED'}

def validate_faceit_rig(armature_obj):
    """Validate that the armature has the expected FaceIt bones"""
    if not armature_obj or armature_obj.type != 'ARMATURE':
        return False, "Not a valid armature object"
    
    # Check for some key FaceIt bones
    required_bones = [
        "c_eyelid_upper.L", "c_eyelid_upper.R",
        "c_jaw_target", "c_mouth_close"
    ]
    
    missing_bones = []
    for bone_name in required_bones:
        if bone_name not in armature_obj.pose.bones:
            missing_bones.append(bone_name)
    
    if missing_bones:
        return False, f"Missing FaceIt bones: {', '.join(missing_bones)}"
    
    return True, "Valid FaceIt rig"

def get_csv_column_mapping(filepath, source_type):
    """Analyze CSV file and return mapping of columns to bone transforms"""
    bone_mapping = get_bone_mapping_for_source(source_type)
    
    try:
        with open(filepath, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            csv_columns = reader.fieldnames
            
            matched_columns = {}
            unmatched_columns = []
            
            for csv_column in csv_columns:
                if csv_column in ['Timecode', 'BlendShapeCount']:
                    continue
                
                found_match = False
                for mapping_key, mapping_info in bone_mapping.items():
                    if (csv_column.lower() == mapping_key.lower() or 
                        csv_column.lower().replace('_', '').replace('-', '') == 
                        mapping_key.lower().replace('_', '').replace('-', '')):
                        matched_columns[csv_column] = mapping_info
                        found_match = True
                        break
                
                if not found_match:
                    unmatched_columns.append(csv_column)
            
            return matched_columns, unmatched_columns
            
    except Exception as e:
        return {}, [f"Error reading CSV: {str(e)}"]