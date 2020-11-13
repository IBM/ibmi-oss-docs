# At top on conf.py (with other import statements)
import recommonmark

# See
# https://github.com/readthedocs/recommonmark/issues/156#issuecomment-607641732
#from recommonmark.transform import AutoStructify

import os
from docutils import nodes
from recommonmark.transform import AutoStructify as AutoStructifyOrig

class AutoStructify(AutoStructifyOrig):
    def parse_ref(self, ref):
        """
        Patch AutoStructify for relative path
        """
        title = None
        if len(ref.children) == 0:
            title = ref['name'] if 'name' in ref else None
        elif isinstance(ref.children[0], nodes.Text):
            title = ref.children[0].astext()
        uri = ref['refuri']
        if uri.find('://') != -1:
            return (title, uri, None)
        anchor = None
        arr = uri.split('#')
        if len(arr) == 2:
            anchor = arr[1]
        if len(arr) > 2 or len(arr[0]) == 0:
            return (title, uri, None)
        uri = arr[0]

        abspath = os.path.abspath(os.path.join(self.file_dir, uri))
        # ** Patch
        if uri[0] != '/': # input uri is relative path
            abspath = '/' + os.path.relpath(abspath, self.root_dir)
        relpath = os.path.relpath(abspath, self.root_dir)

        # use url resolver
        if self.url_resolver:
            uri = self.url_resolver(relpath)
        if anchor:
            uri += '#' + anchor
        return (title, uri, None)

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'IBM i OSS Docs'
copyright = '2020, IBM i OSS Docs Authors'
author = 'IBM i OSS Docs Authors'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'recommonmark',
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    '.licensing',
    'requirements.txt',
]

master_doc = 'README'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

def setup(app):
    app.add_config_value('recommonmark_config', {
            'enable_auto_toc_tree': True,
            'enable_auto_doc_ref': False, # broken in Sphinx 1.6+
            'enable_eval_rst': True,
            'auto_toc_tree_section': 'Contents',
            }, True)
    app.add_transform(AutoStructify)

