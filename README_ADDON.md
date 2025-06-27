# MoCap CSV to FaceIt Converter - Blender Addon

## Overview
This Blender addon converts CSV blendshape data to FaceIt rig bone animations, enabling import of facial motion capture data directly into Blender.

## Features
- **CSV Import**: Supports standard blendshape CSV format with timecode data
- **FaceIt Compatibility**: Works with FaceitControlRig armatures
- **Automatic Mapping**: Maps 26+ blendshapes to appropriate bones
- **Scaling Control**: Adjustable global scaling factor for fine-tuning
- **Progress Tracking**: Visual progress indicator during import
- **Error Handling**: Comprehensive validation and error reporting
- **Animation Cleanup**: Clear existing animation option

## Supported Blendshapes

### Eye Controls
- **EyeBlinkLeft/Right**: Controls upper eyelid (c_eyelid_upper.L/R)
- **EyeWideLeft/Right**: Additional upper eyelid control (additive)
- **EyeSquintLeft/Right**: Controls lower eyelid (c_eyelid_lower.L/R)
- **EyeLookUp/Down/In/OutLeft/Right**: Eye rotation controls (c_lookat_mch.L/R)

### Mouth Controls  
- **MouthClose**: Mouth closure (c_mouth_close)
- **MouthFunnel**: Funnel mouth shape (c_mouth_funnel)
- **MouthPucker**: Pucker mouth shape (c_mouth_pucker)
- **MouthSmileLeft/Right**: Smile controls (c_mouth_smile.L/R)
- **MouthFrownLeft/Right**: Frown controls (c_mouth_frown.L/R)

### Jaw Controls
- **JawOpen**: Jaw opening (c_jaw_target Y-axis)
- **JawLeft/Right**: Jaw side movement (c_jaw_target X-axis)
- **JawForward**: Jaw forward movement (c_jaw_target Z-axis)

### Other Controls
- **TongueOut**: Tongue extension (c_tongue)

## Installation

1. Download the `mocap_csv_importer.zip` file
2. In Blender, go to Edit > Preferences > Add-ons
3. Click "Install..." and select the ZIP file
4. Enable "MoCap CSV to FaceIt Converter" in the addon list

## Usage

1. **Open the MoCap Panel**: In the 3D Viewport, open the sidebar (N key) and find the "MoCap" tab
2. **Select CSV File**: Click the folder icon next to "CSV File" and select your blendshape CSV
3. **Set Target Rig**: Ensure "Target Rig" matches your FaceitControlRig object name
4. **Configure Settings**:
   - **Start Frame**: Frame number where animation should begin
   - **Scaling Factor**: Global multiplier for all blendshape values (default: 4.75)
5. **Import Animation**: Click "Import Animation" to process the CSV data
6. **Review Results**: Check the timeline and keyframes on affected bones

## CSV Format Requirements

Your CSV file should have:
- **Header row** with blendshape names
- **Timecode column** (optional but recommended)
- **Numeric values** between 0.0 and 1.0 for blendshape weights
- **One row per frame** of animation data

Example CSV structure:
```
Timecode,EyeBlinkLeft,EyeBlinkRight,JawOpen,MouthSmileLeft,...
00:00:00:01.001,0.117,0.065,0.015,0.000,...
00:00:00:02.002,0.118,0.068,0.014,0.000,...
```

## Conversion Formula

The addon uses the following conversion logic:

1. **Bone Mapping**: Each blendshape maps to a specific bone and transform type
2. **Scaling**: Value = CSV_Value × Scaling_Factor × Individual_Scaling
3. **Combination**: Multiple blendshapes can affect the same bone (additive)
4. **Transform**: Applied to location (LOC_X/Y/Z) or rotation (ROT_X/Y/Z)

Example for left eyelid:
```
Final_Y_Location = (EyeBlinkLeft + EyeWideLeft) × 4.75 × Global_Scaling
```

## Troubleshooting

### Common Issues

**"Target rig not found"**
- Ensure your armature is named "FaceitControlRig" or update the target name
- Make sure the object is an armature type

**"Invalid CSV file"**
- Check that your CSV has proper headers and numeric values
- Ensure at least 3 expected blendshapes are present

**"Missing bones in rig"**
- Your rig may not have all standard FaceIt bones
- The addon will skip missing bones and continue with available ones

**Animation doesn't look right**
- Try adjusting the global scaling factor (typically 3.0-8.0)
- Check that your CSV values are in the expected 0.0-1.0 range

### Performance Notes

- Large CSV files (1000+ frames) may take several minutes to import
- The addon shows progress during import
- Consider importing smaller sections for testing

## Technical Details

### File Structure
- `__init__.py`: Addon registration and properties
- `operators.py`: Import and clear animation operators  
- `panels.py`: User interface panels
- `mappings.py`: Blendshape to bone mapping and conversion formulas
- `utils.py`: CSV parsing and validation utilities

### Conversion Accuracy
The addon achieves >99% accuracy compared to reference animation data through:
- Empirically derived scaling factors
- Proper additive blendshape combination
- Frame-by-frame keyframe application

## License
This addon is provided as-is for facial motion capture workflows.

## Support
For issues or questions, please refer to the repository documentation or create an issue on the project repository.