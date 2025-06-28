bl_info = {
    "name": "MOCAP Conversion",
    "author": "ranfaranfis",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "File > Import",
    "description": "Import facial motion capture data from CSV files to FaceIt rigs",
    "warning": "",
    "doc_url": "",
    "category": "Import-Export",
}

import bpy
from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper
from . import utils
from . import DIZIONARIO
from . import operators

class ImportMocapCSV(bpy.types.Operator, ImportHelper):
    """Import facial mocap data from CSV file"""
    bl_idname = "import_anim.mocap_csv"
    bl_label = "Import Mocap CSV"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".csv"
    filter_glob: StringProperty(
        default="*.csv",
        options={'HIDDEN'},
        maxlen=255,
    )

    target_object: StringProperty(
        name="Target Object",
        description="Name of the FaceIt control rig object",
        default="FaceitControlRig"
    )

    source_type: bpy.props.EnumProperty(
        name="Source Type",
        description="Type of mocap data source",
        items=[
            ('face_cap', 'Face Cap', 'Face Cap format'),
            ('epic', 'Epic Games', 'Epic Games format'),
            ('a2f', 'Audio2Face', 'Audio2Face format'),
        ],
        default='face_cap'
    )

    use_frame_optimization: BoolProperty(
        name="Optimize Frame Operations",
        description="Use batch keyframe insertion for better performance",
        default=True
    )

    def execute(self, context):
        return utils.import_mocap_csv(
            context,
            self.filepath,
            self.target_object,
            self.source_type,
            self.use_frame_optimization
        )

def menu_func_import(self, context):
    self.layout.operator(ImportMocapCSV.bl_idname, text="Mocap CSV (.csv)")

def register():
    bpy.utils.register_class(ImportMocapCSV)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    operators.register()

def unregister():
    bpy.utils.unregister_class(ImportMocapCSV)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    operators.unregister()

if __name__ == "__main__":
    register()