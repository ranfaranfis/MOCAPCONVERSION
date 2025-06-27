bl_info = {
    "name": "MoCap CSV to FaceIt Converter",
    "author": "MOCAPCONVERSION",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > MoCap",
    "description": "Convert CSV blendshape data to FaceIt rig animation",
    "warning": "",
    "doc_url": "",
    "category": "Animation",
}

import bpy
from . import panels, operators, mappings, utils

classes = (
    operators.MOCAP_OT_import_csv,
    operators.MOCAP_OT_clear_animation,
    panels.MOCAP_PT_csv_importer,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Register properties
    bpy.types.Scene.mocap_csv_file = bpy.props.StringProperty(
        name="CSV File",
        description="Path to the CSV blendshape file",
        default="",
        subtype='FILE_PATH'
    )
    
    bpy.types.Scene.mocap_target_object = bpy.props.StringProperty(
        name="Target Object",
        description="Name of the FaceitControlRig object",
        default="FaceitControlRig"
    )
    
    bpy.types.Scene.mocap_frame_start = bpy.props.IntProperty(
        name="Start Frame",
        description="Frame to start applying animation",
        default=1,
        min=1
    )
    
    bpy.types.Scene.mocap_scaling_factor = bpy.props.FloatProperty(
        name="Scaling Factor",
        description="Global scaling factor for blendshape values",
        default=4.75,  # Adjusted to better match reference data
        min=0.1,
        max=50.0
    )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    # Unregister properties
    del bpy.types.Scene.mocap_csv_file
    del bpy.types.Scene.mocap_target_object
    del bpy.types.Scene.mocap_frame_start
    del bpy.types.Scene.mocap_scaling_factor

if __name__ == "__main__":
    register()