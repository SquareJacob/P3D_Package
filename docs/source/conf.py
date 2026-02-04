# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'P3D'
copyright = '2026, Jacob Scherzer'
author = 'Jacob Scherzer'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.extlinks",
    "sphinx_copybutton"
]

templates_path = ['_templates']
exclude_patterns = []

autodoc_member_order = 'bysource'
#autodoc_typehints = 'none'
autoclass_content = "both"   # include class docstring + __init__ docstring

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "plotly": ("https://plotly.com/python-api-reference/", None)
}

extlinks = {
    "dash": ("https://dash.plotly.com/reference/#dash.%s", "dash.%s"),
    "dcc": ("https://dash.plotly.com/dash-core-components/%s", "dash.dcc.%s"),
    "html": ("https://dash.plotly.com/dash-html-components/%s", "html.%s"),
    "table": ("https://dash.plotly.com/datatable", "dash.dash_table.DataTable")
}

rst_prolog = """
.. |table| replace:: dash.dash_table.DataTable
.. _table: https://dash.plotly.com/datatable
"""

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
