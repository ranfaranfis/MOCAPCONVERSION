import bpy
from bpy.types import Panel


class MOCAP_PT_csv_importer(Panel):
    """Main panel for CSV import functionality"""
    bl_label = "MoCap CSV Importer"
    bl_idname = "MOCAP_PT_csv_importer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "MoCap"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Header
        row = layout.row()
        row.label(text="CSV to FaceIt Animation", icon='ANIM_DATA')
        
        layout.separator()
        
        # File selection
        box = layout.box()
        box.label(text="Input Settings:", icon='FILEBROWSER')
        
        row = box.row()
        row.prop(scene, "mocap_csv_file", text="CSV File")
        
        row = box.row()
        row.prop(scene, "mocap_target_object", text="Target Rig")
        
        # Animation settings
        box = layout.box()
        box.label(text="Animation Settings:", icon='KEYINGSET')
        
        row = box.row()
        row.prop(scene, "mocap_frame_start", text="Start Frame")
        
        row = box.row()
        row.prop(scene, "mocap_scaling_factor", text="Scaling Factor")
        
        layout.separator()
        
        # Validation info
        if scene.mocap_csv_file:
            from .utils import validate_csv_format, get_faceit_rig_object
            
            is_valid, message = validate_csv_format(scene.mocap_csv_file)
            
            box = layout.box()
            if is_valid:
                box.label(text="✓ CSV File Valid", icon='CHECKMARK')
            else:
                box.label(text="✗ CSV File Invalid", icon='ERROR')
                row = box.row()
                row.label(text=message, icon='INFO')
            
            # Check target object
            target_obj = get_faceit_rig_object(scene.mocap_target_object)
            if target_obj:
                box.label(text=f"✓ Found rig: {target_obj.name}", icon='CHECKMARK')
            else:
                box.label(text="✗ Target rig not found", icon='ERROR')
            
            layout.separator()
        
        # Import button
        row = layout.row(align=True)
        row.scale_y = 2.0
        
        if scene.mocap_csv_file and bpy.path.abspath(scene.mocap_csv_file):
            row.operator("mocap.import_csv", text="Import Animation", icon='PLAY')
        else:
            row.enabled = False
            row.operator("mocap.import_csv", text="Select CSV File First", icon='FILEBROWSER')
        
        # Clear animation button
        row = layout.row(align=True)
        row.operator("mocap.clear_animation", text="Clear Animation", icon='X')
        
        layout.separator()
        
        # Info section
        box = layout.box()
        box.label(text="Instructions:", icon='INFO')
        col = box.column(align=True)
        col.label(text="1. Select your CSV blendshape file")
        col.label(text="2. Ensure FaceitControlRig is in scene")
        col.label(text="3. Adjust scaling factor if needed")
        col.label(text="4. Click Import Animation")
        
        layout.separator()
        
        # Status info
        box = layout.box()
        box.label(text="Supported Blendshapes:", icon='MESH_DATA')
        col = box.column(align=True)
        
        blendshapes = [
            "EyeBlinkLeft/Right", "EyeWideLeft/Right",
            "EyeSquintLeft/Right", "EyeLookUp/Down/In/Out",
            "MouthClose/Funnel/Pucker", "MouthSmile/Frown",
            "JawOpen/Left/Right/Forward", "TongueOut"
        ]
        
        for i in range(0, len(blendshapes), 2):
            row = col.row()
            row.label(text=f"• {blendshapes[i]}")
            if i + 1 < len(blendshapes):
                row.label(text=f"• {blendshapes[i + 1]}")