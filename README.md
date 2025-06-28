# MOCAP Conversion Addon

A Blender addon for importing facial motion capture data from CSV files to FaceIt control rigs.

## 🚀 **CRITICAL BUGS FIXED**

This addon addresses the critical issues identified in the original problem statement:

### ✅ **1. Fixed Pose Bone Transform Application**
- **Problem**: `bone.location = Vector()` didn't persist properly in Blender
- **Solution**: Implemented proper bone matrix manipulation in `apply_transform_to_bone()`
- **Details**: 
  - Forces context updates with `bpy.context.view_layer.update()`
  - Uses proper pose bone transform assignment
  - Ensures transforms persist correctly across frames

### ✅ **2. Optimized Frame Operations**
- **Problem**: `bpy.context.scene.frame_set(frame_number)` called for EVERY frame made import extremely slow
- **Solution**: Implemented batch keyframe insertion
- **Details**:
  - New `use_frame_optimization` option (enabled by default)
  - Collects all keyframe data first, then applies in batch
  - Uses `keyframe_insert()` with specific frame parameter
  - Avoids repeated `frame_set()` calls

### ✅ **3. Fixed Transform Application Issues**
- **Problem**: Location/rotation not being applied to correct transform space
- **Solution**: Proper bone space transform handling
- **Details**:
  - Clear transforms to start from rest pose
  - Apply transforms in correct bone local space
  - Force matrix updates to ensure persistence
  - Support for all transform types (LOC_X/Y/Z, ROT_X/Y/Z)

## 📁 **File Structure**

```
MOCAPCONVERSION/
├── __init__.py           # Main addon registration and import operator
├── utils.py              # Core functionality with fixed transform application
├── operators.py          # Additional debugging and validation operators
├── DIZIONARIO.py         # Bone mapping data for different mocap sources
├── test_addon.py         # Test script to validate functionality
├── README.md             # This file
├── 20250523_170050_blendshape_data.csv  # Sample CSV data
├── DIZIONARIO.json       # JSON version of bone mapping
└── lista.json            # Additional data file
```

## 🎯 **Features**

### Import Operators
- **File > Import > Mocap CSV**: Main import functionality
- Support for Face Cap, Epic Games, and Audio2Face formats
- Automatic column mapping to FaceIt bones
- Batch keyframe insertion for optimal performance

### Debug Tools (3D Viewport > N-Panel > MOCAP tab)
- **Validate FaceIt Rig**: Check if armature has required bones
- **Preview Bone Mapping**: Analyze CSV files and show mapping
- **Test Bone Transform**: Test individual bone transforms

## 📊 **Supported Data Sources**

1. **Face Cap** (`face_cap`): Standard Face Cap export format
2. **Epic Games** (`epic`): Epic Games MetaHuman format  
3. **Audio2Face** (`a2f`): NVIDIA Audio2Face export format

## 🎮 **Usage**

### Basic Import
1. Open Blender with a FaceIt rig
2. Go to **File > Import > Mocap CSV**
3. Select your CSV file
4. Choose the correct source type
5. Set target object name (default: "FaceitControlRig")
6. Click **Import**

### Advanced Options
- **Target Object**: Name of your FaceIt control rig
- **Source Type**: Format of your mocap data
- **Optimize Frame Operations**: Use batch keyframe insertion (recommended)

### Validation
1. Open the **3D Viewport**
2. Press **N** to open the side panel
3. Go to **MOCAP** tab
4. Use **Validate FaceIt Rig** to check your armature
5. Use **Preview Bone Mapping** to analyze your CSV file

## 🔧 **Technical Details**

### Bone Mapping
The addon uses `DIZIONARIO.py` which contains mappings from blendshape names to:
- **bone**: Target bone name in FaceIt rig
- **object**: Target object name (usually "FaceitControlRig")
- **transform_type**: Type of transform (LOC_X/Y/Z, ROT_X/Y/Z)
- **source**: Data source type (face_cap, epic, a2f)

### Performance Optimizations
- **Batch Processing**: Collects all keyframe data before applying
- **Minimal Frame Changes**: Avoids `frame_set()` calls during import
- **Efficient Keyframing**: Uses `keyframe_insert()` with frame parameter
- **Matrix Updates**: Forces bone matrix updates for reliable transforms

### Error Handling
- Validates target armature exists and is correct type
- Checks for required FaceIt bones
- Handles missing CSV columns gracefully
- Reports progress and errors to user

## 🧪 **Testing**

Run the test script to validate the addon:

```bash
cd /path/to/MOCAPCONVERSION
python test_addon.py
```

Tests include:
- DIZIONARIO data structure validation
- Bone mapping integrity checks
- CSV format validation
- Utils function structure verification

## 📈 **Expected Results**

After implementing these fixes:

✅ **All blendshapes from CSV apply correctly to bones**  
✅ **Fast import (no more "takes forever")**  
✅ **Complete facial animation instead of just random eye/mouth movement**  
✅ **Proper bone transform persistence**  
✅ **Efficient batch keyframe insertion**  

## 🔍 **Troubleshooting**

### Common Issues

1. **"Object not found" error**
   - Ensure your FaceIt rig is named correctly
   - Use the validation tool to check your rig

2. **"No bone mapping found" error**
   - Verify you selected the correct source type
   - Use preview mapping to check CSV compatibility

3. **Transforms not applying**
   - Check that your rig has the expected FaceIt bone names
   - Use the test transform tool to verify individual bones

4. **Slow import**
   - Ensure "Optimize Frame Operations" is enabled
   - Check console for any error messages

### Debug Tools
- Use the **MOCAP** panel in the 3D viewport for validation
- Check Blender's console for detailed error messages
- Use **Preview Bone Mapping** to verify CSV format

## 🔗 **Compatibility**

- **Blender**: 3.0+
- **FaceIt**: Compatible with FaceIt control rigs
- **Python**: 3.7+

## 📝 **Note**

The reverse engineering values in the bone mapping are correct - the original issue was with the application method, which has now been fixed with proper bone matrix manipulation and optimized frame operations.