import csv
import os
import bpy
from mathutils import Vector, Euler


def parse_csv_file(filepath):
    """
    Parse CSV blendshape file and return frame data
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        List of dictionaries, each containing frame data
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"CSV file not found: {filepath}")
    
    frames = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row_num, row in enumerate(reader):
                try:
                    # Convert timecode to frame number if present
                    frame_data = {}
                    
                    # Copy all blendshape values
                    for key, value in row.items():
                        if key in ['Timecode', 'BlendShapeCount']:
                            frame_data[key] = value
                        else:
                            try:
                                frame_data[key] = float(value)
                            except ValueError:
                                frame_data[key] = 0.0
                    
                    frame_data['frame_number'] = row_num + 1
                    frames.append(frame_data)
                    
                except Exception as e:
                    print(f"Warning: Error parsing row {row_num + 1}: {e}")
                    continue
                    
    except Exception as e:
        raise Exception(f"Error reading CSV file: {e}")
    
    return frames


def get_faceit_rig_object(object_name="FaceitControlRig"):
    """
    Find and return the FaceitControlRig object in the scene
    
    Args:
        object_name: Name of the rig object to find
        
    Returns:
        Blender object or None if not found
    """
    if object_name in bpy.data.objects:
        obj = bpy.data.objects[object_name]
        if obj.type == 'ARMATURE':
            return obj
    
    # Try to find any armature with "faceit" in the name
    for obj in bpy.data.objects:
        if obj.type == 'ARMATURE' and 'faceit' in obj.name.lower():
            return obj
    
    return None


def get_bone_from_armature(armature_obj, bone_name):
    """
    Get a pose bone from the armature
    
    Args:
        armature_obj: Blender armature object
        bone_name: Name of the bone to get
        
    Returns:
        Pose bone or None if not found
    """
    if not armature_obj or armature_obj.type != 'ARMATURE':
        return None
    
    if bone_name in armature_obj.pose.bones:
        return armature_obj.pose.bones[bone_name]
    
    return None


def apply_transform_to_bone(bone, transform_data, frame_number):
    """
    Apply transform data to a bone and set keyframes
    
    Args:
        bone: Blender pose bone
        transform_data: Dictionary with location and rotation data
        frame_number: Frame number to set keyframe at
    """
    if not bone:
        return
    
    # Set current frame
    bpy.context.scene.frame_set(frame_number)
    
    # Apply location
    if transform_data.get("location"):
        bone.location = Vector(transform_data["location"])
        bone.keyframe_insert(data_path="location", frame=frame_number)
    
    # Apply rotation (Euler)
    if transform_data.get("rotation"):
        bone.rotation_euler = Euler(transform_data["rotation"])
        bone.keyframe_insert(data_path="rotation_euler", frame=frame_number)


def validate_csv_format(filepath):
    """
    Validate that the CSV file has the expected format
    
    Args:
        filepath: Path to CSV file
        
    Returns:
        Tuple (is_valid, error_message)
    """
    if not os.path.exists(filepath):
        return False, "File does not exist"
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            headers = reader.fieldnames
            
            if not headers:
                return False, "No headers found in CSV file"
            
            # Check for expected blendshape columns
            expected_blendshapes = [
                'EyeBlinkLeft', 'EyeBlinkRight', 'EyeSquintLeft', 'EyeSquintRight',
                'JawOpen', 'MouthClose', 'MouthSmileLeft', 'MouthSmileRight'
            ]
            
            found_blendshapes = [bs for bs in expected_blendshapes if bs in headers]
            
            if len(found_blendshapes) < 3:
                return False, f"Too few expected blendshapes found. Expected at least 3 of {expected_blendshapes}, found {found_blendshapes}"
            
            # Try to read first row to validate data format
            first_row = next(reader, None)
            if not first_row:
                return False, "CSV file appears to be empty"
            
            # Validate that blendshape values are numeric
            for bs in found_blendshapes:
                try:
                    float(first_row[bs])
                except (ValueError, KeyError):
                    return False, f"Invalid numeric value for blendshape '{bs}' in first row"
            
            return True, "Valid CSV format"
            
    except Exception as e:
        return False, f"Error validating CSV: {e}"


def get_unique_bone_names():
    """
    Get list of unique bone names that will be affected by the mapping
    
    Returns:
        Set of unique bone names
    """
    from .mappings import BONE_MAP
    
    return set(mapping["bone"] for mapping in BONE_MAP.values())


def progress_callback(current, total, message="Processing"):
    """
    Update progress in Blender UI
    
    Args:
        current: Current progress step
        total: Total steps
        message: Progress message
    """
    if total > 0:
        progress = current / total
        print(f"{message}: {current}/{total} ({progress*100:.1f}%)")
        
        # Update Blender's progress indicator if available
        if hasattr(bpy.context.window_manager, 'progress_update'):
            bpy.context.window_manager.progress_update(progress)