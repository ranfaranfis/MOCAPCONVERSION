# Bone mapping and conversion formulas
# Based on DIZIONARIO.py analysis

# Mapping from CSV blendshape names to bone information
# Includes conversion formulas and scaling factors
BONE_MAP = {
    # === EYE BLENDSHAPES ===
    "EyeBlinkLeft": {
        "bone": "c_eyelid_upper.L",
        "object": "FaceitControlRig",
        "transform_type": "LOC_Y",
        "scaling_factor": 4.75,  # Adjusted from 5.0 to better match reference data
        "additive": True  # Can be combined with other blendshapes
    },
    "EyeWideLeft": {
        "bone": "c_eyelid_upper.L",
        "object": "FaceitControlRig", 
        "transform_type": "LOC_Y",
        "scaling_factor": 4.75,  # Adjusted from 5.0
        "additive": True
    },
    "EyeBlinkRight": {
        "bone": "c_eyelid_upper.R",
        "object": "FaceitControlRig",
        "transform_type": "LOC_Y", 
        "scaling_factor": 4.75,  # Adjusted from 5.0
        "additive": True
    },
    "EyeWideRight": {
        "bone": "c_eyelid_upper.R",
        "object": "FaceitControlRig",
        "transform_type": "LOC_Y",
        "scaling_factor": 4.75,  # Adjusted from 5.0
        "additive": True
    },
    "EyeSquintLeft": {
        "bone": "c_eyelid_lower.L",
        "object": "FaceitControlRig",
        "transform_type": "LOC_Y",
        "scaling_factor": 4.75,  # Adjusted from 5.0
        "additive": True
    },
    "EyeSquintRight": {
        "bone": "c_eyelid_lower.R",
        "object": "FaceitControlRig",
        "transform_type": "LOC_Y",
        "scaling_factor": 4.75,  # Adjusted from 5.0
        "additive": True
    },
    
    # === EYE LOOK BLENDSHAPES ===
    "EyeLookUpLeft": {
        "bone": "c_lookat_mch.L",
        "object": "FaceitControlRig",
        "transform_type": "ROT_X",
        "scaling_factor": 1.0,
        "additive": True
    },
    "EyeLookUpRight": {
        "bone": "c_lookat_mch.R", 
        "object": "FaceitControlRig",
        "transform_type": "ROT_X",
        "scaling_factor": 1.0,
        "additive": True
    },
    "EyeLookDownLeft": {
        "bone": "c_lookat_mch.L",
        "object": "FaceitControlRig",
        "transform_type": "ROT_X",
        "scaling_factor": -1.0,  # Negative for opposite direction
        "additive": True
    },
    "EyeLookDownRight": {
        "bone": "c_lookat_mch.R",
        "object": "FaceitControlRig", 
        "transform_type": "ROT_X",
        "scaling_factor": -1.0,
        "additive": True
    },
    "EyeLookInLeft": {
        "bone": "c_lookat_mch.L",
        "object": "FaceitControlRig",
        "transform_type": "ROT_Z",
        "scaling_factor": 1.0,
        "additive": True
    },
    "EyeLookInRight": {
        "bone": "c_lookat_mch.R",
        "object": "FaceitControlRig",
        "transform_type": "ROT_Z", 
        "scaling_factor": 1.0,
        "additive": True
    },
    "EyeLookOutLeft": {
        "bone": "c_lookat_mch.L",
        "object": "FaceitControlRig",
        "transform_type": "ROT_Z",
        "scaling_factor": -1.0,
        "additive": True
    },
    "EyeLookOutRight": {
        "bone": "c_lookat_mch.R",
        "object": "FaceitControlRig",
        "transform_type": "ROT_Z",
        "scaling_factor": -1.0,
        "additive": True
    },
    
    # === MOUTH BLENDSHAPES ===
    "MouthClose": {
        "bone": "c_mouth_close",
        "object": "FaceitControlRig",
        "transform_type": "LOC_Z",
        "scaling_factor": 3.0,
        "additive": False
    },
    "MouthFunnel": {
        "bone": "c_mouth_funnel",
        "object": "FaceitControlRig",
        "transform_type": "LOC_Z",
        "scaling_factor": 3.0,
        "additive": False
    },
    "MouthPucker": {
        "bone": "c_mouth_pucker",
        "object": "FaceitControlRig",
        "transform_type": "LOC_Z",
        "scaling_factor": 3.0,
        "additive": False
    },
    "MouthSmileLeft": {
        "bone": "c_mouth_smile.L",
        "object": "FaceitControlRig",
        "transform_type": "ROT_Z",
        "scaling_factor": 2.0,
        "additive": False
    },
    "MouthSmileRight": {
        "bone": "c_mouth_smile.R",
        "object": "FaceitControlRig",
        "transform_type": "ROT_Z",
        "scaling_factor": 2.0,
        "additive": False
    },
    "MouthFrownLeft": {
        "bone": "c_mouth_frown.L",
        "object": "FaceitControlRig",
        "transform_type": "ROT_Z",
        "scaling_factor": 2.0,
        "additive": False
    },
    "MouthFrownRight": {
        "bone": "c_mouth_frown.R",
        "object": "FaceitControlRig",
        "transform_type": "ROT_Z",
        "scaling_factor": 2.0,
        "additive": False
    },
    
    # === JAW BLENDSHAPES ===
    "JawOpen": {
        "bone": "c_jaw_target",
        "object": "FaceitControlRig",
        "transform_type": "LOC_Y",
        "scaling_factor": 3.0,
        "additive": True
    },
    "JawRight": {
        "bone": "c_jaw_target",
        "object": "FaceitControlRig",
        "transform_type": "LOC_X",
        "scaling_factor": 3.0,
        "additive": True
    },
    "JawLeft": {
        "bone": "c_jaw_target",
        "object": "FaceitControlRig",
        "transform_type": "LOC_X",
        "scaling_factor": -3.0,  # Negative for opposite direction
        "additive": True
    },
    "JawForward": {
        "bone": "c_jaw_target",
        "object": "FaceitControlRig",
        "transform_type": "LOC_Z",
        "scaling_factor": 3.0,
        "additive": True
    },
    
    # === TONGUE BLENDSHAPES ===
    "TongueOut": {
        "bone": "c_tongue",
        "object": "FaceitControlRig",
        "transform_type": "LOC_Y",
        "scaling_factor": 2.0,
        "additive": False
    }
}

def get_transform_axis(transform_type):
    """Get the axis index for the transform type"""
    if transform_type in ["LOC_X", "ROT_X"]:
        return 0
    elif transform_type in ["LOC_Y", "ROT_Y"]:
        return 1
    elif transform_type in ["LOC_Z", "ROT_Z"]:
        return 2
    return 0

def calculate_bone_transform(csv_row, bone_name, global_scaling=1.0):
    """
    Calculate the final transform value for a bone based on CSV data
    
    Args:
        csv_row: Dictionary containing CSV blendshape values
        bone_name: Name of the target bone
        global_scaling: Global scaling factor
    
    Returns:
        Dictionary with transform data: {"location": [x,y,z], "rotation": [x,y,z]}
    """
    result = {
        "location": [0.0, 0.0, 0.0],
        "rotation": [0.0, 0.0, 0.0]
    }
    
    # Find all blendshapes that affect this bone
    affecting_blendshapes = []
    for csv_key, mapping in BONE_MAP.items():
        if mapping["bone"] == bone_name and csv_key in csv_row:
            affecting_blendshapes.append((csv_key, mapping))
    
    # Group by transform type and axis
    location_values = [0.0, 0.0, 0.0]
    rotation_values = [0.0, 0.0, 0.0]
    
    for csv_key, mapping in affecting_blendshapes:
        csv_value = float(csv_row[csv_key])
        scaling = mapping["scaling_factor"] * global_scaling
        axis = get_transform_axis(mapping["transform_type"])
        final_value = csv_value * scaling
        
        if mapping["transform_type"].startswith("LOC"):
            if mapping.get("additive", False):
                location_values[axis] += final_value
            else:
                location_values[axis] = final_value
        elif mapping["transform_type"].startswith("ROT"):
            if mapping.get("additive", False):
                rotation_values[axis] += final_value
            else:
                rotation_values[axis] = final_value
    
    result["location"] = location_values
    result["rotation"] = rotation_values
    
    return result