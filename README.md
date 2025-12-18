pytextools
=========

A small toolbox to help generate LaTeX files (figures and tables) from Python code and pandas DataFrames.

Summary
-------
- Author: Thomas Ingeman-Nielsen
- License: GNU General Public License (GPL)
- Key runtime dependency: pandas, numpy

What it does
------------
pytextools provides helper routines to append figures, tables and section/chapter headings to LaTeX files. It is designed to work with pandas DataFrames (for `append_table`) and uses numpy in a few formatting helpers.

Notable public functions
- append_figure(file, figfilepath, ...)
- append_table(file, df, ...)
- append_section_heading(file, secname, ...)
- append_chapter_title(file, title, ...)
- create_dirs(dir_list)
- with_file(f, func, ...)
- fixed(x, sig=3), scientific(x, sig=3, tex=True)

Quick example
-------------
```python
import pandas as pd
import pytextools as pt

# Write a simple LaTeX file with a table
df = pd.DataFrame([['Name','Value'], ['A', 1], ['B', 2]])
with open('example.tex', 'w') as f:
    pt.append_section_heading(f, 'Example')
    pt.append_table(f, df, index=False, header=['Parameter','Value'])
```

Installation
------------
Below are PowerShell commands for Windows (adjust for other shells).

Development install
- Create and activate a virtual environment, then install editable package and developer deps.

```powershell
# create and activate venv (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# install developer dependencies (requirements.txt)
python -m pip install -r requirements.txt

# install package in editable/develop mode
python -m pip install -e .
```

Notes:
- If you run into build errors relating to `numpy` during installation, pre-install numpy into the environment first:

```powershell
python -m pip install numpy
python -m pip install -e .
```

Production install
- To install the package for production use from local source (build wheel and install):

```powershell
# build a wheel (this will use pyproject.toml build-system requires)
python -m pip wheel . -w dist

# install the built wheel
python -m pip install dist\pytextools-0.1.0-py3-none-any.whl
```

- Or install directly (pip will build/resolve dependencies automatically):

```powershell
python -m pip install .
```

Requirements and pins
---------------------
- `pyproject.toml` declares `pandas` as a runtime dependency and `numpy` as a build-time requirement. This is appropriate because the package code imports pandas at runtime, while the build/setup uses numpy.
- For reproducible developer environments, pin versions in `requirements.txt` (e.g., `pandas==2.3.2`, `numpy==2.3.3`). For published packages, prefer minimum-version constraints in `pyproject.toml` (e.g., `pandas>=1.5`).

Troubleshooting
---------------
- Build fails with "No module named 'numpy'": install numpy into your environment first (`python -m pip install numpy`) or ensure pip can install build requirements (internet access and a recent pip).
- If LaTeX output contains unexpected characters, check `escape` settings passed to `append_table` and whether headers are already LaTeX-escaped.

License
-------
This project is released under the GNU General Public License (GPL). See `pyproject.toml` for the license text field.
