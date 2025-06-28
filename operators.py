import bpy
from bpy.props import StringProperty, EnumProperty
from . import utils
from . import DIZIONARIO

class ValidateFaceitRig(bpy.types.Operator):
    """Validate that the selected armature is a compatible FaceIt rig"""
    bl_idname = "mocap.validate_faceit_rig"
    bl_label = "Validate FaceIt Rig"
    bl_options = {'REGISTER'}

    target_object: StringProperty(
        name="Target Object",
        description="Name of the FaceIt control rig object",
        default="FaceitControlRig"
    )

    def execute(self, context):
        if self.target_object not in bpy.data.objects:
            self.report({'ERROR'}, f"Object '{self.target_object}' not found")
            return {'CANCELLED'}
        
        armature_obj = bpy.data.objects[self.target_object]
        is_valid, message = utils.validate_faceit_rig(armature_obj)
        
        if is_valid:
            self.report({'INFO'}, f"✓ {message}")
        else:
            self.report({'WARNING'}, f"⚠ {message}")
        
        return {'FINISHED'}

class PreviewBoneMapping(bpy.types.Operator):
    """Preview which CSV columns will map to which bones"""
    bl_idname = "mocap.preview_bone_mapping"
    bl_label = "Preview Bone Mapping"
    bl_options = {'REGISTER'}

    csv_filepath: StringProperty(
        name="CSV File",
        description="Path to CSV file to analyze",
        subtype='FILE_PATH'
    )

    source_type: EnumProperty(
        name="Source Type",
        description="Type of mocap data source",
        items=[
            ('face_cap', 'Face Cap', 'Face Cap format'),
            ('epic', 'Epic Games', 'Epic Games format'),
            ('a2f', 'Audio2Face', 'Audio2Face format'),
        ],
        default='face_cap'
    )

    def execute(self, context):
        if not self.csv_filepath:
            self.report({'ERROR'}, "Please select a CSV file")
            return {'CANCELLED'}
        
        matched, unmatched = utils.get_csv_column_mapping(self.csv_filepath, self.source_type)
        
        print("="*50)
        print(f"BONE MAPPING PREVIEW ({self.source_type})")
        print("="*50)
        
        if matched:
            print(f"✓ MATCHED COLUMNS ({len(matched)}):")
            for csv_col, bone_info in matched.items():
                print(f"  {csv_col} → {bone_info['bone']} ({bone_info['transform_type']})")
        
        if unmatched:
            print(f"\n⚠ UNMATCHED COLUMNS ({len(unmatched)}):")
            for col in unmatched:
                print(f"  {col}")
        
        self.report({'INFO'}, f"Mapping analysis complete. Matched: {len(matched)}, Unmatched: {len(unmatched)}")
        return {'FINISHED'}

class TestSingleBoneTransform(bpy.types.Operator):
    """Test applying a transform to a single bone"""
    bl_idname = "mocap.test_bone_transform"
    bl_label = "Test Bone Transform"
    bl_options = {'REGISTER', 'UNDO'}

    target_object: StringProperty(
        name="Target Object",
        description="Name of the FaceIt control rig object",
        default="FaceitControlRig"
    )

    bone_name: StringProperty(
        name="Bone Name",
        description="Name of the bone to test",
        default="c_jaw_target"
    )

    transform_type: EnumProperty(
        name="Transform Type",
        description="Type of transform to apply",
        items=[
            ('LOC_X', 'Location X', 'Location X'),
            ('LOC_Y', 'Location Y', 'Location Y'),
            ('LOC_Z', 'Location Z', 'Location Z'),
            ('ROT_X', 'Rotation X', 'Rotation X'),
            ('ROT_Y', 'Rotation Y', 'Rotation Y'),
            ('ROT_Z', 'Rotation Z', 'Rotation Z'),
        ],
        default='LOC_Y'
    )

    value: bpy.props.FloatProperty(
        name="Value",
        description="Transform value to apply",
        default=0.1,
        min=-10.0,
        max=10.0
    )

    def execute(self, context):
        if self.target_object not in bpy.data.objects:
            self.report({'ERROR'}, f"Object '{self.target_object}' not found")
            return {'CANCELLED'}
        
        armature_obj = bpy.data.objects[self.target_object]
        
        success = utils.apply_transform_to_bone(
            armature_obj, 
            self.bone_name, 
            self.transform_type, 
            self.value
        )
        
        if success:
            self.report({'INFO'}, f"Applied {self.transform_type}={self.value} to {self.bone_name}")
        else:
            self.report({'ERROR'}, f"Failed to apply transform to {self.bone_name}")
        
        return {'FINISHED'}

class MocapToolsPanel(bpy.types.Panel):
    """Panel for MOCAP conversion tools"""
    bl_label = "MOCAP Conversion Tools"
    bl_idname = "VIEW3D_PT_mocap_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'MOCAP'

    def draw(self, context):
        layout = self.layout
        
        # Validation section
        box = layout.box()
        box.label(text="Validation:", icon='CHECKMARK')
        box.operator("mocap.validate_faceit_rig")
        
        # Preview section
        box = layout.box()
        box.label(text="Preview Mapping:", icon='PREVIEW_RANGE')
        box.operator("mocap.preview_bone_mapping")
        
        # Testing section
        box = layout.box()
        box.label(text="Test Transform:", icon='BONE_DATA')
        box.operator("mocap.test_bone_transform")

def register():
    bpy.utils.register_class(ValidateFaceitRig)
    bpy.utils.register_class(PreviewBoneMapping)
    bpy.utils.register_class(TestSingleBoneTransform)
    bpy.utils.register_class(MocapToolsPanel)

def unregister():
    bpy.utils.unregister_class(ValidateFaceitRig)
    bpy.utils.unregister_class(PreviewBoneMapping)
    bpy.utils.unregister_class(TestSingleBoneTransform)
    bpy.utils.unregister_class(MocapToolsPanel)