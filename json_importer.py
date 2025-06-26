import bpy
import json
import time

print("Starting JSON-based mocap import...")

def import_from_json(json_file_path):
    """Import animation data from JSON file."""
    start_time = time.time()
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        print(f"Loaded JSON data: {data['metadata']['exported_frames']} frames")
        
        keyframes_inserted = 0
        total_frames = len(data['animation_data'])
        
        for i, frame_data in enumerate(data['animation_data']):
            frame_num = frame_data['frame']
            
            for blendshape_name, blendshape_data in frame_data['blendshapes'].items():
                try:
                    obj_name = blendshape_data['object']
                    bone_name = blendshape_data['bone']
                    transform_type = blendshape_data['transform_type']
                    value = blendshape_data['value']
                    
                    # Get object
                    obj = bpy.data.objects.get(obj_name)
                    if not obj:
                        continue
                    
                    # Set object as active
                    bpy.context.view_layer.objects.active = obj
                    
                    # Set value and insert keyframe
                    if transform_type.startswith('LOC_'):
                        axis = transform_type.split('_')[1].lower()
                        axis_index = {'x': 0, 'y': 1, 'z': 2}[axis]
                        obj.pose.bones[bone_name].location[axis_index] = value
                        data_path = f'pose.bones["{bone_name}"].location'
                        obj.keyframe_insert(data_path=data_path, index=axis_index, frame=frame_num)
                    elif transform_type.startswith('ROT_'):
                        axis = transform_type.split('_')[1].lower()
                        axis_index = {'x': 0, 'y': 1, 'z': 2}[axis]
                        obj.pose.bones[bone_name].rotation_euler[axis_index] = value
                        data_path = f'pose.bones["{bone_name}"].rotation_euler'
                        obj.keyframe_insert(data_path=data_path, index=axis_index, frame=frame_num)
                    
                    keyframes_inserted += 1
                    
                except Exception as e:
                    print(f"Error processing {blendshape_name}: {e}")
                    continue
            
            # Progress update
            if i % 50 == 0:
                progress = (i + 1) / total_frames * 100
                print(f"Progress: {progress:.1f}% ({i+1}/{total_frames} frames)")
        
        print(f"Import completed: {keyframes_inserted} keyframes in {time.time() - start_time:.2f} seconds")
        
        # Update scene frame range
        if data['animation_data']:
            max_frame = max(frame['frame'] for frame in data['animation_data'])
            bpy.context.scene.frame_end = max_frame
            print(f"Scene frame range updated to: 1 - {max_frame}")
        
    except Exception as e:
        print(f"Error importing JSON data: {e}")
        raise

# Import the data
import_from_json("mocap_data.json")
print("JSON import completed!")
