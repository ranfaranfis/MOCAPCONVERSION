"""
Example usage of the MOCAP Conversion addon functionality.
This script demonstrates how to use the core functions programmatically.

NOTE: This requires Blender with the addon installed to run.
"""

import bpy
from . import utils
from . import DIZIONARIO

def example_import_csv():
    """Example of importing a CSV file programmatically"""
    
    # File paths (adjust as needed)
    csv_filepath = "/path/to/your/mocap_data.csv"
    target_object_name = "FaceitControlRig"
    source_type = "face_cap"  # or "epic" or "a2f"
    use_optimization = True
    
    # Import the mocap data
    result = utils.import_mocap_csv(
        bpy.context,
        csv_filepath,
        target_object_name,
        source_type,
        use_optimization
    )
    
    if result == {'FINISHED'}:
        print("✓ Import completed successfully!")
    else:
        print("✗ Import failed!")

def example_test_single_bone():
    """Example of testing a single bone transform"""
    
    # Get the armature object
    armature_obj = bpy.data.objects.get("FaceitControlRig")
    if not armature_obj:
        print("FaceitControlRig not found!")
        return
    
    # Test jaw open animation
    success = utils.apply_transform_to_bone(
        armature_obj,
        "c_jaw_target",    # Bone name
        "LOC_Y",           # Transform type
        0.1,               # Value
        frame=1            # Frame number
    )
    
    if success:
        print("✓ Bone transform applied successfully!")
    else:
        print("✗ Bone transform failed!")

def example_validate_rig():
    """Example of validating a FaceIt rig"""
    
    armature_obj = bpy.data.objects.get("FaceitControlRig")
    if not armature_obj:
        print("FaceitControlRig not found!")
        return
    
    is_valid, message = utils.validate_faceit_rig(armature_obj)
    
    if is_valid:
        print(f"✓ Rig validation: {message}")
    else:
        print(f"✗ Rig validation: {message}")

def example_preview_mapping():
    """Example of previewing bone mapping for a CSV file"""
    
    csv_filepath = "/path/to/your/mocap_data.csv"
    source_type = "face_cap"
    
    matched, unmatched = utils.get_csv_column_mapping(csv_filepath, source_type)
    
    print(f"Matched columns: {len(matched)}")
    for csv_col, bone_info in matched.items():
        print(f"  {csv_col} → {bone_info['bone']} ({bone_info['transform_type']})")
    
    print(f"Unmatched columns: {len(unmatched)}")
    for col in unmatched:
        print(f"  {col}")

def example_get_bone_mapping():
    """Example of getting bone mapping for a specific source type"""
    
    # Get mapping for Face Cap data
    face_cap_mapping = utils.get_bone_mapping_for_source("face_cap")
    print(f"Face Cap mapping has {len(face_cap_mapping)} entries")
    
    # Get mapping for Audio2Face data
    a2f_mapping = utils.get_bone_mapping_for_source("a2f")
    print(f"Audio2Face mapping has {len(a2f_mapping)} entries")
    
    # Get mapping for Epic Games data
    epic_mapping = utils.get_bone_mapping_for_source("epic")
    print(f"Epic Games mapping has {len(epic_mapping)} entries")

def example_batch_keyframes():
    """Example of applying multiple transforms efficiently"""
    
    armature_obj = bpy.data.objects.get("FaceitControlRig")
    if not armature_obj:
        print("FaceitControlRig not found!")
        return
    
    # Apply multiple transforms for animation
    transforms = [
        ("c_jaw_target", "LOC_Y", 0.0, 1),    # Frame 1: Jaw closed
        ("c_jaw_target", "LOC_Y", 0.1, 10),   # Frame 10: Jaw open
        ("c_jaw_target", "LOC_Y", 0.05, 20),  # Frame 20: Jaw half open
        ("c_jaw_target", "LOC_Y", 0.0, 30),   # Frame 30: Jaw closed
    ]
    
    for bone_name, transform_type, value, frame in transforms:
        utils.apply_transform_to_bone(
            armature_obj, bone_name, transform_type, value, frame
        )
    
    print("✓ Batch keyframes applied!")

if __name__ == "__main__":
    # Only run if we're in Blender
    try:
        import bpy
        print("Running MOCAP Conversion examples...")
        
        # Uncomment the examples you want to run:
        # example_validate_rig()
        # example_get_bone_mapping()
        # example_test_single_bone()
        # example_batch_keyframes()
        # example_import_csv()  # Requires valid CSV file path
        # example_preview_mapping()  # Requires valid CSV file path
        
    except ImportError:
        print("This script requires Blender to run!")
        print("Use it as a reference for programmatic usage.")