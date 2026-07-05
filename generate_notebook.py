import os
import json
import glob

def compile_notebook():
    print("Compiling ultimate_python_masterclass.ipynb...")
    topics_dir = os.path.join(os.path.dirname(__file__), "topics")
    if not os.path.exists(topics_dir):
        print(f"Error: {topics_dir} does not exist. Creating it.")
        os.makedirs(topics_dir)
        
    # Get all .py files in topics/ sorted alphabetically
    pattern = os.path.join(topics_dir, "*.py")
    py_files = sorted(glob.glob(pattern))
    
    if not py_files:
        print("No topic files found in topics/ directory.")
        return

    cells = []
    for file_path in py_files:
        filename = os.path.basename(file_path)
        print(f"Adding cell from: {filename}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Standard .ipynb source is a list of lines, each line ending with \n
        lines = content.splitlines(keepends=True)
        
        cell = {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": lines
        }
        cells.append(cell)
        
    notebook = {
        "cells": cells,
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
    
    output_path = os.path.join(os.path.dirname(__file__), "ultimate_python_masterclass.ipynb")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
        
    print(f"Successfully generated {output_path} with {len(cells)} cells.")

if __name__ == "__main__":
    compile_notebook()
