# Configuration file for the Sphinx documentation builder.

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath('..'))  # Permite importar `codigos`

project = 'Cálculo Numérico'
author = 'Pedro Henrique Rocha de Andrade'
copyright = f"{datetime.now().year}, {author}"

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
]

# Napoleon settings (NumPy style)
napoleon_numpy_docstring = True
napoleon_google_docstring = False

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'pt_BR'

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

autosummary_generate = True

# Let autodoc show the docstrings even if the object is not imported
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'