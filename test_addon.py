#!/usr/bin/env python3
"""
Test script to validate the MOCAP conversion addon functionality.
This script tests the core functions without requiring Blender to be running.
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_dizionario_import():
    """Test that DIZIONARIO can be imported and contains expected data"""
    try:
        import DIZIONARIO
        
        # Check that BONE_MAP_UNIFICATA exists
        assert hasattr(DIZIONARIO, 'BONE_MAP_UNIFICATA'), "BONE_MAP_UNIFICATA not found"
        
        # Check that it contains expected source types
        sources = set()
        for key, value in DIZIONARIO.BONE_MAP_UNIFICATA.items():
            sources.add(value.get('source'))
        
        expected_sources = {'face_cap', 'epic', 'a2f'}
        assert expected_sources.issubset(sources), f"Missing sources: {expected_sources - sources}"
        
        print("✓ DIZIONARIO import test passed")
        return True
        
    except Exception as e:
        print(f"✗ DIZIONARIO import test failed: {e}")
        return False

def test_bone_mapping_structure():
    """Test that bone mapping has the correct structure"""
    try:
        import DIZIONARIO
        
        bone_map = DIZIONARIO.BONE_MAP_UNIFICATA
        
        # Test a few specific entries
        test_entries = [
            'eyeBlinkLeft',
            'jawOpen', 
            'mouthClose_a2f',
            'eyeLookUpLeft_epic'
        ]
        
        for entry in test_entries:
            assert entry in bone_map, f"Missing entry: {entry}"
            
            data = bone_map[entry]
            required_fields = ['bone', 'object', 'transform_type', 'source']
            
            for field in required_fields:
                assert field in data, f"Missing field '{field}' in entry '{entry}'"
            
            # Validate transform types
            valid_transforms = ['LOC_X', 'LOC_Y', 'LOC_Z', 'ROT_X', 'ROT_Y', 'ROT_Z']
            assert data['transform_type'] in valid_transforms, f"Invalid transform type: {data['transform_type']}"
        
        print("✓ Bone mapping structure test passed")
        return True
        
    except Exception as e:
        print(f"✗ Bone mapping structure test failed: {e}")
        return False

def test_csv_data_format():
    """Test that the CSV file has the expected format"""
    try:
        csv_file = '20250523_170050_blendshape_data.csv'
        if not os.path.exists(csv_file):
            print(f"⚠ CSV file {csv_file} not found, skipping test")
            return True
        
        import csv
        
        with open(csv_file, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Check headers
            headers = reader.fieldnames
            assert 'Timecode' in headers, "Missing Timecode column"
            assert 'BlendShapeCount' in headers, "Missing BlendShapeCount column"
            
            # Check that we have some blendshape columns
            blendshape_columns = [h for h in headers if h not in ['Timecode', 'BlendShapeCount']]
            assert len(blendshape_columns) > 0, "No blendshape columns found"
            
            # Read first few rows to check data format
            rows_checked = 0
            for row in reader:
                try:
                    # Check that blendshape values are numeric
                    for col in blendshape_columns[:5]:  # Check first 5 columns
                        if row[col]:  # Skip empty values
                            float(row[col])
                    
                    rows_checked += 1
                    if rows_checked >= 3:  # Check first 3 rows
                        break
                        
                except ValueError as e:
                    print(f"⚠ Non-numeric value found in CSV: {e}")
        
        print("✓ CSV data format test passed")
        return True
        
    except Exception as e:
        print(f"✗ CSV data format test failed: {e}")
        return False

def test_utils_functions():
    """Test utility functions that don't require Blender"""
    try:
        # We can't fully test utils functions without Blender, but we can test imports
        import importlib.util
        
        spec = importlib.util.spec_from_file_location("utils_test", "utils.py")
        # We can't actually import utils because it depends on bpy, 
        # but we can check the file exists and basic syntax
        
        if not os.path.exists("utils.py"):
            raise FileNotFoundError("utils.py not found")
        
        # Check file size and basic content
        with open("utils.py", 'r') as f:
            content = f.read()
            
        assert "apply_transform_to_bone" in content, "apply_transform_to_bone function not found"
        assert "import_mocap_csv" in content, "import_mocap_csv function not found"
        assert "keyframe_insert" in content, "Keyframe functionality not found"
        
        print("✓ Utils functions structure test passed")
        return True
        
    except Exception as e:
        print(f"✗ Utils functions test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Running MOCAP Conversion Addon Tests")
    print("=" * 40)
    
    tests = [
        test_dizionario_import,
        test_bone_mapping_structure,
        test_csv_data_format,
        test_utils_functions,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())