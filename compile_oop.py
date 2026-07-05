import os
import json
import glob

def compile_oop_notebooks():
    print("Compiling Python_OOP_Master notebooks...")
    base_dir = os.path.dirname(__file__)
    sources_dir = os.path.join(base_dir, "oop_sources")
    output_dir = os.path.join(base_dir, "Python_OOP_Master")
    
    if not os.path.exists(sources_dir):
        print(f"Creating source directory: {sources_dir}")
        os.makedirs(sources_dir)
        
    if not os.path.exists(output_dir):
        print(f"Creating output directory: {output_dir}")
        os.makedirs(output_dir)
        
    py_files = sorted(glob.glob(os.path.join(sources_dir, "*.py")))
    if not py_files:
        print("No source files found in oop_sources/.")
        return
        
    for py_file in py_files:
        filename = os.path.basename(py_file)
        name_without_ext = os.path.splitext(filename)[0]
        output_filename = f"{name_without_ext}.ipynb"
        output_path = os.path.join(output_dir, output_filename)
        
        print(f"Compiling: {filename} -> {output_filename}")
        
        with open(py_file, "r", encoding="utf-8") as f:
            content = f.read()
            
        lines = content.splitlines(keepends=True)
        
        # Build the single-cell notebook structure
        notebook = {
            "cells": [
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": lines
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3 (ipykernel)",
                    "language": "python",
                    "name": "python3"
                },
                "language_info": {
                    "codemirror_mode": {
                        "name": "ipython",
                        "version": 3
                    },
                    "file_extension": ".py",
                    "mimetype": "text/x-python",
                    "name": "python",
                    "nbconvert_exporter": "python",
                    "pygments_lexer": "ipython3",
                    "version": "3.12.0"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 2
        }
        
        with open(output_path, "w", encoding="utf-8") as out_f:
            json.dump(notebook, out_f, indent=1, ensure_ascii=False)
            
    print(f"Compilation finished. Output saved in {output_dir}.")

if __name__ == "__main__":
    compile_oop_notebooks()
