#!/usr/bin/env python3
"""
GUI Application for Motion Capture CSV to Bone Data Conversion
Uses tkinter for the interface and converts CSV motion capture data 
to bone transformations based on the DIZIONARIO mapping.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import json
import os
from typing import Dict, List, Optional, Any
import traceback

# Import the dictionary from the existing file
try:
    from DIZIONARIO import BONE_MAP_UNIFICATA
except ImportError:
    messagebox.showerror("Error", "Could not load DIZIONARIO.py. Make sure the file exists in the same directory.")
    exit(1)


class MotionCaptureConverter:
    """Main GUI application for motion capture data conversion."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Motion Capture CSV Converter")
        self.root.geometry("1000x700")
        
        # Application state
        self.csv_data: Optional[pd.DataFrame] = None
        self.csv_file_path: str = ""
        self.current_frame: int = 0
        self.max_frames: int = 0
        self.source_filter: str = "all"
        self.processed_data: Dict[str, Any] = {}
        
        # Create the GUI
        self.create_widgets()
        self.update_display()
        
    def create_widgets(self):
        """Create and layout all GUI widgets."""
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # File selection section
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="5")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Button(file_frame, text="Select CSV File", 
                  command=self.select_csv_file).grid(row=0, column=0, padx=(0, 10))
        
        self.file_label = ttk.Label(file_frame, text="No file selected")
        self.file_label.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Frame selection section
        frame_frame = ttk.LabelFrame(main_frame, text="Frame Selection", padding="5")
        frame_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        frame_frame.columnconfigure(1, weight=1)
        
        ttk.Label(frame_frame, text="Frame:").grid(row=0, column=0, padx=(0, 10))
        
        # Frame slider
        self.frame_var = tk.IntVar()
        self.frame_scale = ttk.Scale(frame_frame, from_=0, to=0, 
                                   variable=self.frame_var, orient=tk.HORIZONTAL,
                                   command=self.on_frame_change)
        self.frame_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Frame input
        self.frame_entry = ttk.Entry(frame_frame, width=10, textvariable=self.frame_var)
        self.frame_entry.grid(row=0, column=2, padx=(0, 10))
        self.frame_entry.bind('<Return>', self.on_frame_entry_change)
        
        # Frame info
        self.frame_info_label = ttk.Label(frame_frame, text="0 / 0")
        self.frame_info_label.grid(row=0, column=3)
        
        # Source filter section
        source_frame = ttk.LabelFrame(main_frame, text="Source Filter", padding="5")
        source_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.source_var = tk.StringVar(value="all")
        source_options = [("All", "all"), ("Face Cap", "face_cap"), ("Epic", "epic"), ("A2F", "a2f")]
        
        for i, (text, value) in enumerate(source_options):
            ttk.Radiobutton(source_frame, text=text, variable=self.source_var, 
                           value=value, command=self.on_source_change).grid(row=0, column=i, padx=10)
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="5")
        results_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Create treeview for results
        columns = ("Parameter", "Value", "Bone", "Object", "Transform", "Source")
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=15)
        
        # Configure column headings and widths
        self.results_tree.heading("Parameter", text="Parameter")
        self.results_tree.heading("Value", text="Value")
        self.results_tree.heading("Bone", text="Bone")
        self.results_tree.heading("Object", text="Object")
        self.results_tree.heading("Transform", text="Transform")
        self.results_tree.heading("Source", text="Source")
        
        self.results_tree.column("Parameter", width=150)
        self.results_tree.column("Value", width=100)
        self.results_tree.column("Bone", width=150)
        self.results_tree.column("Object", width=150)
        self.results_tree.column("Transform", width=100)
        self.results_tree.column("Source", width=100)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        h_scrollbar = ttk.Scrollbar(results_frame, orient=tk.HORIZONTAL, command=self.results_tree.xview)
        self.results_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid the treeview and scrollbars
        self.results_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Export section
        export_frame = ttk.Frame(main_frame)
        export_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Button(export_frame, text="Export to JSON", 
                  command=self.export_to_json).pack(side=tk.LEFT, padx=(0, 10))
        
        self.export_status_label = ttk.Label(export_frame, text="")
        self.export_status_label.pack(side=tk.LEFT)
        
    def select_csv_file(self):
        """Open file dialog to select CSV file."""
        file_path = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.load_csv_file(file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load CSV file:\n{str(e)}")
                
    def load_csv_file(self, file_path: str):
        """Load and validate CSV file."""
        try:
            # Load CSV data
            self.csv_data = pd.read_csv(file_path)
            self.csv_file_path = file_path
            
            # Validate CSV structure
            if self.csv_data.empty:
                raise ValueError("CSV file is empty")
                
            # Update UI
            self.file_label.config(text=f"Loaded: {os.path.basename(file_path)}")
            
            # Set frame range
            self.max_frames = len(self.csv_data) - 1
            self.frame_scale.config(to=self.max_frames)
            self.frame_var.set(0)
            self.current_frame = 0
            
            # Update display
            self.update_frame_info()
            self.process_current_frame()
            
        except Exception as e:
            raise Exception(f"Error loading CSV file: {str(e)}")
            
    def on_frame_change(self, value=None):
        """Handle frame slider change."""
        if self.csv_data is not None:
            self.current_frame = int(float(value))
            self.process_current_frame()
            
    def on_frame_entry_change(self, event=None):
        """Handle frame entry change."""
        if self.csv_data is not None:
            try:
                frame_num = int(self.frame_var.get())
                if 0 <= frame_num <= self.max_frames:
                    self.current_frame = frame_num
                    self.frame_scale.set(frame_num)
                    self.process_current_frame()
                else:
                    messagebox.showwarning("Invalid Frame", 
                                         f"Frame must be between 0 and {self.max_frames}")
                    self.frame_var.set(self.current_frame)
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter a valid frame number")
                self.frame_var.set(self.current_frame)
                
    def on_source_change(self):
        """Handle source filter change."""
        self.source_filter = self.source_var.get()
        if self.csv_data is not None:
            self.process_current_frame()
            
    def process_current_frame(self):
        """Process the current frame and update results display."""
        if self.csv_data is None or self.current_frame >= len(self.csv_data):
            return
            
        try:
            # Get current frame data
            frame_data = self.csv_data.iloc[self.current_frame]
            
            # Process data according to dictionary mapping
            self.processed_data = self.convert_frame_data(frame_data)
            
            # Update display
            self.update_results_display()
            self.update_frame_info()
            
        except Exception as e:
            messagebox.showerror("Processing Error", f"Error processing frame {self.current_frame}:\n{str(e)}")
            
    def convert_frame_data(self, frame_data: pd.Series) -> Dict[str, Any]:
        """Convert frame data using the bone mapping dictionary."""
        results = {
            "frame": self.current_frame,
            "timecode": frame_data.get("Timecode", ""),
            "bones": {}
        }
        
        # Process each column in the CSV
        for column_name in frame_data.index:
            if column_name in ["Timecode", "BlendShapeCount"]:
                continue
                
            value = frame_data[column_name]
            if pd.isna(value) or value == 0:
                continue
                
            # Look for matching entries in the dictionary
            found_match = False
            
            # Check direct match first
            if column_name in BONE_MAP_UNIFICATA:
                bone_info = BONE_MAP_UNIFICATA[column_name]
                if self.should_include_source(bone_info["source"]):
                    self.add_bone_data(results["bones"], column_name, value, bone_info)
                    found_match = True
            
            # Check alternative naming if no direct match found
            if not found_match:
                alt_names = self.get_alternative_names(column_name)
                for alt_name in alt_names:
                    if alt_name in BONE_MAP_UNIFICATA:
                        bone_info = BONE_MAP_UNIFICATA[alt_name]
                        if self.should_include_source(bone_info["source"]):
                            self.add_bone_data(results["bones"], alt_name, value, bone_info)
                            found_match = True
                            break
            
            # Check with source suffixes if still no match
            if not found_match:
                for source in ["_face_cap", "_epic", "_a2f"]:
                    key_with_suffix = column_name + source
                    if key_with_suffix in BONE_MAP_UNIFICATA:
                        bone_info = BONE_MAP_UNIFICATA[key_with_suffix]
                        if self.should_include_source(bone_info["source"]):
                            self.add_bone_data(results["bones"], key_with_suffix, value, bone_info)
                            found_match = True
                            break
                        
        return results
        
    def get_alternative_names(self, column_name: str) -> List[str]:
        """Get alternative names for a column to handle naming variations."""
        alternatives = []
        
        if column_name:
            # Convert PascalCase to camelCase (e.g., EyeBlinkLeft -> eyeBlinkLeft)
            camel_case = column_name[0].lower() + column_name[1:] if len(column_name) > 0 else column_name
            alternatives.append(camel_case)
            
            # Convert from PascalCase/CamelCase to snake_case
            snake_case = ''.join(['_' + c.lower() if c.isupper() else c for c in column_name]).lstrip('_')
            alternatives.append(snake_case)
            
            # Add source suffixes to both camel case and snake case
            for source in ["face_cap", "epic", "a2f"]:
                alternatives.append(f"{camel_case}_{source}")
                alternatives.append(f"{snake_case}_{source}")
                
        return alternatives
        
    def should_include_source(self, source: str) -> bool:
        """Check if the source should be included based on current filter."""
        return self.source_filter == "all" or self.source_filter == source
        
    def add_bone_data(self, bones_dict: Dict, param_name: str, value: float, bone_info: Dict):
        """Add bone data to the results dictionary."""
        bone_name = bone_info["bone"]
        
        if bone_name not in bones_dict:
            bones_dict[bone_name] = {
                "object": bone_info["object"],
                "transforms": {}
            }
            
        bones_dict[bone_name]["transforms"][param_name] = {
            "value": float(value),
            "transform_type": bone_info["transform_type"],
            "source": bone_info["source"]
        }
        
    def update_results_display(self):
        """Update the results treeview with current processed data."""
        # Clear existing items
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
            
        if not self.processed_data or "bones" not in self.processed_data:
            return
            
        # Organize data by bone
        bones_data = self.processed_data["bones"]
        
        for bone_name, bone_data in sorted(bones_data.items()):
            # Add bone as parent item
            bone_item = self.results_tree.insert("", "end", text=bone_name, values=(
                f"BONE: {bone_name}", "", "", bone_data["object"], "", ""
            ))
            
            # Add transforms as child items
            for param_name, transform_data in sorted(bone_data["transforms"].items()):
                self.results_tree.insert(bone_item, "end", values=(
                    param_name,
                    f"{transform_data['value']:.6f}",
                    bone_name,
                    bone_data["object"],
                    transform_data["transform_type"],
                    transform_data["source"]
                ))
                
        # Expand all items
        for item in self.results_tree.get_children():
            self.results_tree.item(item, open=True)
            
    def update_frame_info(self):
        """Update frame information display."""
        self.frame_info_label.config(text=f"{self.current_frame} / {self.max_frames}")
        
    def update_display(self):
        """Update the entire display based on current state."""
        if self.csv_data is None:
            # Disable controls when no file is loaded
            self.frame_scale.config(state="disabled")
            self.frame_entry.config(state="disabled")
        else:
            # Enable controls when file is loaded
            self.frame_scale.config(state="normal")
            self.frame_entry.config(state="normal")
            
    def export_to_json(self):
        """Export current processed data to JSON file."""
        if not self.processed_data:
            messagebox.showwarning("No Data", "No data to export. Please load a CSV file and select a frame.")
            return
            
        try:
            # Ask user for save location
            file_path = filedialog.asksaveasfilename(
                title="Save JSON file",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.processed_data, f, indent=2, ensure_ascii=False)
                    
                self.export_status_label.config(text=f"Exported: {os.path.basename(file_path)}")
                messagebox.showinfo("Export Successful", f"Data exported to:\n{file_path}")
                
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export data:\n{str(e)}")


def main():
    """Main function to run the application."""
    root = tk.Tk()
    app = MotionCaptureConverter(root)
    root.mainloop()


if __name__ == "__main__":
    main()