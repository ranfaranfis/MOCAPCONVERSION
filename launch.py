#!/usr/bin/env python3
"""
Launcher script for the Motion Capture CSV Converter GUI application.
This script provides a simple way to start the application with proper error handling.
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import traceback

def check_dependencies():
    """Check if all required dependencies are available."""
    missing = []
    
    try:
        import pandas
    except ImportError:
        missing.append("pandas")
    
    try:
        import tkinter
    except ImportError:
        missing.append("tkinter")
    
    return missing

def check_files():
    """Check if required files are present."""
    required_files = ["DIZIONARIO.py", "mocap_gui.py"]
    missing = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    return missing

def main():
    """Main launcher function."""
    print("🚀 Motion Capture CSV Converter Launcher")
    print("=" * 50)
    
    # Check dependencies
    print("📦 Checking dependencies...")
    missing_deps = check_dependencies()
    if missing_deps:
        print(f"❌ Missing dependencies: {', '.join(missing_deps)}")
        print("💡 Install with: pip install " + " ".join(missing_deps))
        return 1
    else:
        print("✅ All dependencies found")
    
    # Check files
    print("📁 Checking required files...")
    missing_files = check_files()
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        print("💡 Make sure you're running from the correct directory")
        return 1
    else:
        print("✅ All required files found")
    
    # Import and launch the application
    try:
        print("🎨 Starting GUI application...")
        from mocap_gui import main as gui_main
        gui_main()
        print("👋 Application closed normally")
        return 0
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Check that all files are in the same directory")
        return 1
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("📝 Full error details:")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    
    if exit_code != 0:
        input("\nPress Enter to exit...")
    
    sys.exit(exit_code)