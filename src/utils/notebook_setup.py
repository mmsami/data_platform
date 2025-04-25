# src/utils/notebook_setup.py
import sys
from pathlib import Path

def setup_notebook():
    notebook_dir = Path.cwd()
    if notebook_dir.name == 'notebooks':
        project_root = str(notebook_dir.parent)
        if project_root not in sys.path:
            sys.path.append(project_root)