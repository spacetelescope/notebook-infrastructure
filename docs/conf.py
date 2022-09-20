# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'notebook-infrastructure'
copyright = "2022, STScI's notebook infrastructure team"
author = "STScI's notebook infrastructure team"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['myst_parser']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

html_theme_options = {
    'logo': 'stsci_pri_combo_mark_white_bkgd.png',
    'github_user': 'spacetelescope',
    'github_repo': 'notebook-infrastructure',
}
html_favicon = '_static/stsci_favicon.ico'

html_context = {
  'display_github': True,
  'github_user': 'spacetelescope',
  'github_repo': 'notebook-infrastructure',
  'github_version': 'main',
}