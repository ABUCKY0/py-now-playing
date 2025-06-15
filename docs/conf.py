# -- Project information -----------------------------------------------------
from pathlib import Path
import sys
project = 'Py Now Playing'
author = 'ABUCKY0'
release = '0.2.0'
copyright = "2025, ABUCKY0"
html_theme = 'furo'
extensions = [
    'myst_parser',
    'sphinx.ext.autodoc'
]


sys.path.insert(0, str(Path('..').resolve()))
