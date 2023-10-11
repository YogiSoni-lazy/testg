# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


from labs import version as labs_version

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'DynoLabs'
copyright = '2023, Red Hat Product and Technical Learning'
author = 'Red Hat Product and Technical Learning'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.napoleon'
]

templates_path = ['_templates']
exclude_patterns = []

# The version info for the project,
# Use |version| or |release| in the docs to show the version
#
# The short X.Y version.
version = labs_version.__version__
# The full version
release = labs_version.__version__

myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "replacements",
    "smartquotes",
    "substitution",
    "tasklist",
]

myst_substitutions = {
    "version": version,
    "core_version_badge": f"[![rht-labs-core](https://img.shields.io/badge/rht--labs--core-{version}-blue)]"
    "(https://github.com/RedHatTraining/rht-labs-core)"
}

# Allow links to repo files as
# <repo:src/labs/lab.py>
myst_url_schemes = {
    "http": None,
    "https": None,
    "repo": {
        "url": "https://github.com/RedHatTraining/rht-labs-core/blob/master/{{path}}",
        "title": "{{path}}"
    }
}

# -- Options for intersphinx -------------------------------------------------
#

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ['_static']

html_favicon = "_static/favicon.ico"
html_theme_options = {
    "source_repository": "https://github.com/RedHatTraining/rht-labs-core",
    "source_branch": "master",
    "source_directory": "docs/source",
    "light_logo": "DynoLabs.png",
    "dark_logo": "DynoLabs-Dynamic.png",
    # You can add HTML code in the announcement
    "announcement": "",
    "sidebar_hide_name": True
}

# -- Options for autodoc ----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#configuration

# Automatically extract typehints when specified and place them in
# descriptions of the relevant function/method.
autodoc_typehints = "description"

# Don't show class signature with the class' name.
autodoc_class_signature = "separated"
