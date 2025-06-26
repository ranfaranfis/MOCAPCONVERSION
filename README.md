# CSV to FaceIt Rig Animation Converter

A complete Python tool that converts CSV blendshape data to FaceIt rig animations. This tool is completely autonomous with all conversions hardcoded for seamless operation.

## Features

- ✅ **Complete Autonomous Operation**: All mappings and conversion values are hardcoded
- ✅ **FaceIt Rig Support**: Targets all major FaceIt control bones
- ✅ **Full Facial Control Support**: Eyes, mouth, eyebrows, jaw, nose, cheeks, and more
- ✅ **Multiple Export Formats**: Blender Python scripts and JSON data
- ✅ **Precise Transformations**: Maintains exact proportions and scaling
- ✅ **Timecode Handling**: Proper frame timing and rate conversion
- ✅ **Simple Interface**: Load CSV → Get applied animation

## Supported Blendshapes

The tool supports 43 blendshape controls mapped to 30 FaceIt rig bones:

### Eye Controls
- `EyeBlinkLeft` / `EyeBlinkRight` → `c_eyelid_upper.L/R`
- `EyeSquintLeft` / `EyeSquintRight` → `c_eyelid_lower.L/R`
- `EyeWideLeft` / `EyeWideRight` → `c_eyelid_upper.L/R`
- `EyeLookUpLeft` / `EyeLookUpRight` → `c_lookat_mch.L/R` (ROT_X)
- `EyeLookDownLeft` / `EyeLookDownRight` → `c_lookat_mch.L/R` (ROT_X)
- `EyeLookInLeft` / `EyeLookInRight` → `c_lookat_mch.L/R` (ROT_Z)
- `EyeLookOutLeft` / `EyeLookOutRight` → `c_lookat_mch.L/R` (ROT_Z)

### Mouth Controls
- `MouthClose` → `c_mouth_close`
- `MouthFunnel` → `c_mouth_funnel`
- `MouthPucker` → `c_mouth_pucker`
- `MouthSmileLeft` / `MouthSmileRight` → `c_mouth_smile.L/R`
- `MouthFrownLeft` / `MouthFrownRight` → `c_mouth_frown.L/R`
- `MouthStretchLeft` / `MouthStretchRight` → `c_lips_corner_adjust.L/R`
- `MouthRight` / `MouthLeft` → `c_jaw_target` (LOC_X)
- `MouthDimpleLeft` / `MouthDimpleRight` → `c_mouth_smile.L/R`
- `MouthRollLower` / `MouthRollUpper` → `c_lips_lower/upper`
- `MouthShrugLower` / `MouthShrugUpper` → `c_lips_lower/upper`
- `MouthPressLeft` / `MouthPressRight` → `c_lips_corner.L/R`

### Jaw Controls
- `JawOpen` → `c_jaw_target` (LOC_Y)
- `JawRight` / `JawLeft` → `c_jaw_target` (LOC_X)
- `JawForward` → `c_jaw_target` (LOC_Z)

### Eyebrow Controls
- `BrowDownLeft` / `BrowDownRight` → `c_brow_lower.L/R`
- `BrowInnerUp` → `c_brow_inner`
- `BrowOuterUpLeft` / `BrowOuterUpRight` → `c_brow_outer.L/R`

### Additional Controls
- `TongueOut` → `c_tongue`
- `CheekPuff` → `c_cheek.L`
- `CheekSquintLeft` / `CheekSquintRight` → `c_cheek.L/R`
- `NoseSneerLeft` / `NoseSneerRight` → `c_nose.L/R`

## Installation

No installation required! The tool is a standalone Python script with minimal dependencies.

### Requirements
- Python 3.6 or higher
- Standard library modules only (csv, json, math, argparse, pathlib, typing, dataclasses)

## Usage

### Basic Usage

```bash
# Convert CSV to Blender script (default)
python csv_to_rig_converter.py your_blendshape_data.csv

# Convert CSV to JSON format
python csv_to_rig_converter.py your_blendshape_data.csv --format json

# Specify custom output file
python csv_to_rig_converter.py input.csv --output my_animation.py

# Show conversion summary
python csv_to_rig_converter.py input.csv --summary
```

### Command Line Options

```
python csv_to_rig_converter.py [-h] [--output OUTPUT] [--format {blender,json}] [--summary] input_csv

positional arguments:
  input_csv             Input CSV file with blendshape data

options:
  --output OUTPUT, -o OUTPUT
                        Output file path
  --format {blender,json}, -f {blender,json}
                        Output format (default: blender)
  --summary, -s         Show conversion summary
```

## CSV Format

The tool expects CSV files with the following structure:

```csv
Timecode,BlendShapeCount,EyeBlinkLeft,EyeLookDownLeft,...
00:00:00:01.001,51,0.11733060,0.18357788,...
00:00:00:02.002,51,0.11780734,0.19833963,...
```

### Required Columns
- `Timecode`: Frame timing in HH:MM:SS:FF.fff format
- `BlendShapeCount`: Number of blendshapes (informational)
- Blendshape columns with exact names matching the supported list above

## Output Formats

### Blender Python Script (.py)
Generates a complete Blender Python script that can be executed directly in Blender:

```python
import bpy
from mathutils import Vector, Euler, Quaternion

def apply_faceit_animation():
    """Apply animation to FaceIt rig."""
    # Script automatically applies keyframes to all relevant bones
```

**Usage in Blender:**
1. Open Blender with your FaceIt rig
2. Open the Text Editor
3. Load and run the generated script
4. Animation will be applied automatically

### JSON Format (.json)
Exports structured animation data for custom applications:

```json
{
  "metadata": {
    "frame_count": 411,
    "frame_rate": 30.0,
    "source": "CSV to Rig Converter",
    "rig_type": "FaceIt"
  },
  "frames": {
    "1": {
      "timecode": "00:00:00:01.001",
      "bones": {
        "c_eyelid_upper.L": {
          "location": [0.0, 0.24510036, 0.0],
          "rotation_quaternion": [1.0, 0.0, 0.0, 0.0],
          "rotation_euler": [0.0, 0.0, 0.0],
          "scale": [1.0, 1.0, 1.0]
        }
      }
    }
  }
}
```

## Analysis Tool

Use the included animation inspector to validate your generated data:

```bash
python animation_inspector.py your_animation.json
```

This provides detailed statistics including:
- Active vs inactive bones
- Transform value ranges
- Frame coverage per bone
- Animation duration and metadata

## Example Output

```
=== Animation Data Analysis Report ===

Source: CSV to Rig Converter
Rig Type: FaceIt
Frame Rate: 30.0 FPS
Total Frames: 410
Duration: 13.67 seconds

Total Bones: 30
Active Bones: 24

Active Bones (with movement):
  - c_eyelid_upper.L: active in 410 frames (100.0%)
  - c_jaw_target: active in 410 frames (100.0%)
  - c_mouth_smile.L: active in 407 frames (99.3%)
  ...
```

## Conversion Details

### Hardcoded Scaling Factors
The tool applies these scaling factors for optimal FaceIt compatibility:

```python
scaling_factors = {
    "LOC_X": 0.1,    # Lateral movement
    "LOC_Y": 2.0,    # Forward/backward movement  
    "LOC_Z": 1.0,    # Up/down movement
    "ROT_X": 0.5,    # Pitch rotation
    "ROT_Y": 0.5,    # Yaw rotation
    "ROT_Z": 0.3,    # Roll rotation
}
```

### Transform Limits
Automatic clamping ensures safe bone transformations:
- Location: ±10.0 units
- Rotation: ±π radians

### Frame Rate
- Default: 30 FPS
- Timecode parsing supports HH:MM:SS:FF.fff format
- Automatic frame number calculation

## Architecture

### Main Classes

- **`CSVToRigConverter`**: Main converter class with hardcoded mappings
- **`Transform`**: Dataclass for bone transformation data
- **`FrameData`**: Dataclass for per-frame animation data

### Key Methods

- `parse_csv()`: Reads and processes CSV blendshape data
- `apply_blendshape_to_transform()`: Converts blendshape values to bone transforms
- `export_to_blender_script()`: Generates Blender Python script
- `export_to_json()`: Exports structured JSON data

## Error Handling

The tool includes robust error handling for:
- Missing or malformed CSV files
- Invalid blendshape values
- Unsupported blendshape names
- File I/O errors
- Transform limit violations

## Examples

### Sample Workflow

1. **Export blendshape data** from your mocap system as CSV
2. **Convert to Blender script**:
   ```bash
   python csv_to_rig_converter.py mocap_data.csv
   ```
3. **Load in Blender** and run the generated script
4. **Verify animation** using the inspector:
   ```bash
   python animation_inspector.py mocap_data.json
   ```

### Batch Processing

```bash
# Process multiple CSV files
for file in *.csv; do
    python csv_to_rig_converter.py "$file" --format json
done
```

## Compatibility

- **Blender**: 2.80+ (uses modern Python API)
- **FaceIt**: Compatible with standard FaceIt rig structure
- **Python**: 3.6+ required for dataclasses support
- **CSV**: Standard RFC 4180 compliant format

## Performance

- **Memory Efficient**: Processes frames incrementally
- **Fast Conversion**: ~1000 frames per second typical performance
- **Scalable**: Handles animations of any length

## Troubleshooting

### Common Issues

1. **"No values applied"**: Check blendshape column names match exactly
2. **"Missing bones"**: Ensure FaceIt rig is properly named and structured
3. **"Invalid timecode"**: Verify CSV timecode format is HH:MM:SS:FF.fff

### Debugging

Enable debug mode by adding print statements to track blendshape processing:

```python
# Add to apply_blendshape_to_transform method
print(f"Processing {blendshape_name}: {value} -> {bone_name}")
```

## Contributing

The tool is designed to be completely self-contained. To add new blendshapes:

1. Add mapping to `_get_bone_mappings()`
2. Test with sample CSV data
3. Verify output with animation inspector

## License

This tool is provided as-is for mocap to FaceIt rig conversion workflows.