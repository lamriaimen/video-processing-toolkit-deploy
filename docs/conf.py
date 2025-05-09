#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
<<<<<<< HEAD
sys.path.insert(0, os.path.abspath('../src'))
=======
import types
>>>>>>> 9f59c49 (Configure AutoAPI docs, update index.rst, and add Pages CI workflow)

# -- Path setup --------------------------------------------------------------

# Point Sphinx at your package source code
sys.path.insert(0, os.path.abspath('../src'))

# Mock heavy or missing external dependencies so imports in your code won't fail
for _mod in ("cv2", "numpy", "torch", "ffmpy"):
    sys.modules[_mod] = types.ModuleType(_mod)

<<<<<<< HEAD
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]
# Automatically document members (functions, classes, etc.)
autodoc_default_options = {
    'members': True,
    'undoc-members': False,    # set True if you also want undocumented members
    'show-inheritance': True,
}

=======
# Now it's safe to import your package
import video_processing_toolkit  # noqa: E402
>>>>>>> 9f59c49 (Configure AutoAPI docs, update index.rst, and add Pages CI workflow)

# -- Project information -----------------------------------------------------

project = 'Video Processing Toolkit'
author = 'Alyssia Fourali, Loic Scoth, Mohamed Said Aimen Lamri, Gaspar Henniaux'
copyright = f'2025, {author}'
version = video_processing_toolkit.__version__
release = video_processing_toolkit.__version__

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',      # Core: pull in docstrings
    'sphinx.ext.napoleon',     # Supports NumPy/Google style
    'sphinx.ext.viewcode',     # Add “View source” links
    'autoapi.extension',       # AutoAPI for full API reference
]

# AutoAPI settings
autoapi_type = 'python'
autoapi_dirs = [os.path.abspath('../src/video_processing_toolkit')]
autoapi_options = [
    'members',
    'undoc-members',
    'show-inheritance',
    'private-members',
    'imported-members',
]
autoapi_keep_files = True
autoapi_generate_api_docs = True

# In case autodoc still needs to mock imports too
autodoc_mock_imports = ['cv2', 'numpy', 'torch', 'ffmpy']

autodoc_default_options = {
    'members': True,
    'undoc-members': False,
    'show-inheritance': True,
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- HTML output -------------------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
