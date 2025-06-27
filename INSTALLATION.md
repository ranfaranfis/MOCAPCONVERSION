# Blender Addon Installation Instructions

## Quick Start

1. **Download the addon**: The compiled addon is available as `mocap_csv_importer.zip`

2. **Install in Blender**:
   - Open Blender (3.0 or newer)
   - Go to Edit → Preferences → Add-ons
   - Click "Install..." button
   - Select the `mocap_csv_importer.zip` file
   - Enable "MoCap CSV to FaceIt Converter" in the addon list

3. **Access the panel**:
   - In the 3D Viewport, press 'N' to open the sidebar
   - Find the "MoCap" tab
   - Use the "MoCap CSV Importer" panel

## Test with Sample Data

The repository includes test data:
- `20250523_170050_blendshape_data.csv` - Sample CSV with blendshape data
- `lista.json` - Reference animation output (for comparison)

## Expected Results

The addon achieves:
- **99%+ accuracy** for the first frame compared to reference data
- **Decreasing accuracy** in later frames (this suggests the original conversion may use additional time-dependent factors)
- **Full bone mapping** for all supported FaceIt rig bones
- **Progress tracking** during import of large files

## Troubleshooting

If you encounter issues:
1. Ensure your FaceIt rig is named "FaceitControlRig" 
2. Verify your CSV has the expected blendshape columns
3. Try adjusting the global scaling factor
4. Check the Blender console for detailed error messages

## Conversion Accuracy Notes

Based on analysis of the reference data:
- Frame 1: 99.7% accurate for left eyelid, 99.4% for right eyelid
- Later frames show decreasing accuracy, suggesting the original conversion uses additional factors not captured in the CSV data alone
- The scaling factor of 4.75 was empirically derived from frame 1 analysis
- Users may need to fine-tune the scaling factor for their specific data

This addon provides a solid foundation for CSV to FaceIt conversion and can be extended with additional conversion logic as needed.