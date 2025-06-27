import bpy
from bpy.types import Operator
from bpy.props import StringProperty
import os
from .utils import (
    parse_csv_file, 
    get_faceit_rig_object, 
    get_bone_from_armature,
    apply_transform_to_bone,
    validate_csv_format,
    get_unique_bone_names,
    progress_callback
)
from .mappings import calculate_bone_transform


class MOCAP_OT_import_csv(Operator):
    """Import CSV blendshape data and apply to FaceIt rig"""
    bl_idname = "mocap.import_csv"
    bl_label = "Import CSV Animation"
    bl_description = "Import CSV blendshape data and convert to bone animation"
    bl_options = {'REGISTER', 'UNDO'}
    
    filepath: StringProperty(
        name="File Path",
        description="Path to the CSV file",
        subtype='FILE_PATH'
    )
    
    def execute(self, context):
        scene = context.scene
        
        # Get file path
        csv_file = scene.mocap_csv_file
        if not csv_file:
            csv_file = self.filepath
        
        if not csv_file:
            self.report({'ERROR'}, "No CSV file selected")
            return {'CANCELLED'}
        
        # Validate file
        is_valid, error_message = validate_csv_format(csv_file)
        if not is_valid:
            self.report({'ERROR'}, f"Invalid CSV file: {error_message}")
            return {'CANCELLED'}
        
        # Get target armature
        target_obj = get_faceit_rig_object(scene.mocap_target_object)
        if not target_obj:
            self.report({'ERROR'}, f"Target armature '{scene.mocap_target_object}' not found")
            return {'CANCELLED'}
        
        # Set target object as active
        bpy.context.view_layer.objects.active = target_obj
        bpy.ops.object.mode_set(mode='POSE')
        
        try:
            # Parse CSV data
            self.report({'INFO'}, "Parsing CSV file...")
            frame_data = parse_csv_file(csv_file)
            
            if not frame_data:
                self.report({'ERROR'}, "No data found in CSV file")
                return {'CANCELLED'}
            
            total_frames = len(frame_data)
            start_frame = scene.mocap_frame_start
            global_scaling = scene.mocap_scaling_factor
            
            self.report({'INFO'}, f"Processing {total_frames} frames starting at frame {start_frame}")
            
            # Get unique bones that will be affected
            unique_bones = get_unique_bone_names()
            affected_bones = {}
            
            # Pre-validate bones exist
            missing_bones = []
            for bone_name in unique_bones:
                bone = get_bone_from_armature(target_obj, bone_name)
                if bone:
                    affected_bones[bone_name] = bone
                else:
                    missing_bones.append(bone_name)
            
            if missing_bones:
                self.report({'WARNING'}, f"Missing bones in rig: {', '.join(missing_bones)}")
            
            if not affected_bones:
                self.report({'ERROR'}, "No valid bones found in target rig")
                return {'CANCELLED'}
            
            # Clear existing keyframes for affected bones
            self.report({'INFO'}, "Clearing existing keyframes...")
            for bone_name, bone in affected_bones.items():
                bone.location = (0.0, 0.0, 0.0)
                bone.rotation_euler = (0.0, 0.0, 0.0)
                bone.keyframe_insert(data_path="location", frame=start_frame - 1)
                bone.keyframe_insert(data_path="rotation_euler", frame=start_frame - 1)
            
            # Process each frame
            successful_frames = 0
            
            # Start progress
            if hasattr(context.window_manager, 'progress_begin'):
                context.window_manager.progress_begin(0, total_frames)
            
            try:
                for frame_idx, csv_row in enumerate(frame_data):
                    current_frame = start_frame + frame_idx
                    
                    # Update progress
                    progress_callback(frame_idx + 1, total_frames, "Importing frames")
                    
                    try:
                        # Process each affected bone
                        for bone_name in affected_bones.keys():
                            # Calculate transform for this bone
                            transform_data = calculate_bone_transform(
                                csv_row, bone_name, global_scaling
                            )
                            
                            # Apply transform to bone
                            bone = affected_bones[bone_name]
                            apply_transform_to_bone(bone, transform_data, current_frame)
                        
                        successful_frames += 1
                        
                    except Exception as e:
                        self.report({'WARNING'}, f"Error processing frame {current_frame}: {e}")
                        continue
                
            finally:
                # End progress
                if hasattr(context.window_manager, 'progress_end'):
                    context.window_manager.progress_end()
            
            # Set timeline to imported range
            context.scene.frame_start = start_frame
            context.scene.frame_end = start_frame + successful_frames - 1
            context.scene.frame_set(start_frame)
            
            # Success message
            self.report({'INFO'}, 
                f"Successfully imported {successful_frames}/{total_frames} frames to {len(affected_bones)} bones")
            
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Import failed: {e}")
            return {'CANCELLED'}
    
    def invoke(self, context, event):
        # If no file is set, open file browser
        if not context.scene.mocap_csv_file:
            context.window_manager.fileselect_add(self)
            return {'RUNNING_MODAL'}
        else:
            return self.execute(context)


class MOCAP_OT_clear_animation(Operator):
    """Clear imported animation data"""
    bl_idname = "mocap.clear_animation"
    bl_label = "Clear Animation"
    bl_description = "Clear all animation data from affected bones"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        
        # Get target armature
        target_obj = get_faceit_rig_object(scene.mocap_target_object)
        if not target_obj:
            self.report({'ERROR'}, f"Target armature '{scene.mocap_target_object}' not found")
            return {'CANCELLED'}
        
        # Set target object as active
        bpy.context.view_layer.objects.active = target_obj
        bpy.ops.object.mode_set(mode='POSE')
        
        try:
            # Get unique bones
            unique_bones = get_unique_bone_names()
            cleared_bones = 0
            
            for bone_name in unique_bones:
                bone = get_bone_from_armature(target_obj, bone_name)
                if bone:
                    # Clear keyframes
                    bone.location = (0.0, 0.0, 0.0)
                    bone.rotation_euler = (0.0, 0.0, 0.0)
                    
                    # Remove all keyframes for this bone
                    if target_obj.animation_data and target_obj.animation_data.action:
                        action = target_obj.animation_data.action
                        
                        # Find and remove fcurves for this bone
                        for fcurve in action.fcurves[:]:  # Copy list to avoid modification during iteration
                            if bone_name in fcurve.data_path:
                                action.fcurves.remove(fcurve)
                    
                    cleared_bones += 1
            
            self.report({'INFO'}, f"Cleared animation from {cleared_bones} bones")
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Clear animation failed: {e}")
            return {'CANCELLED'}