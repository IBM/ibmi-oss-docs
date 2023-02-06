# Python usage notes

```{toctree}
:maxdepth: 1
```

All things assume you have [PATH set correctly](../troubleshooting/SETTING_PATH.md)

## Which versions are available?
Currently, Python versions 3.6 and 3.9 are available, 
via the `python3` and `python39` packages, respectively.

**Important Note**
Performing a `yum upgrade` operation will not upgrade
currently-installed versions of Python to a new major
version. This would break existing apps. 

## Python virtual environments (highly recommended!)
### 1. Installing system-wide packages
Use `yum` to install any RPM-provided packages that you
may use inside your virtual environment. 

### 2. Creating a virtual environment
**If using Python 3.9**
```
python3.9 -m venv --system-site-packages /path/to/venv
```
**If using Python 3.6**
```
python3.6 -m venv --system-site-packages /path/to/venv
```
### 3. Entering and using the virtual environment
To "enter" a virtual environment, run:
```
source /path/to/venv/bin/activate
```
Once completed, you should be able to run the `python` and `pip` commands. They will use the version of Python that was used to create the virtual environment. 


## Which Python command to use outside of a virtual environment?
### Python interpreter

**Use the versioned python command when feasible.**
It is always best to run the fully-versioned python command, which is
either `python3.9` or `python3.6`, since the `python` or
`python3` commands may render different results depending
on what packages are installed or what the current environment
contains.



**Alternatives if `python39` is not installed**
Use `python3.6`. One can alternatively use the shorthand
`python3`, but including the major and minor version
in the python command is more explicit and is best practice.
For instance, launch your python program via:
```
python3.6 myprogram.py
```

**Alternatives if `python39` is installed** 
Use `python3.9` or simply `python`, since the `python39` package
creates a `python` via `update-alternatives`. 
```
python3.9 myprogram.py
```

### Preferred Installer for Python (pip)
Invoke the Python interpreter command (above), followed
by `-m pip`. For instance:
```
python3.9 -m pip install --upgrade xlsxwriter
```

## Installing Python packages
See [Installing Python Packages](INSTALLING_PYTHON_PKGS.md)

## Modules for accessing Db2, RPG, CL etc

- Be sure to use the `itoolkit` package from PyPI (installable via pip) for accessing RPG, CL, etc.
- For database access with `odbc`:
    -  if running on IBM i: Install the `python3-pyodbc` or `python39-pyodbc` RPM package, depending on which version of Python you are using. This will be much easier than installing with `pip`, which will require you to compile these components. 
    -  If connceting remotely: install `pyodbc` through any supported method, and use the IBM i Access ODBC driver.
    -  (see [the ODBC doc](../odbc/README.md) for further guidance on ODBC).
- For database access with `ibm_db`:
    -  if running on IBM i: install the `python3-ibm_db` or `python39-ibm_db` RPM package, depending on which version of Python you are using. **DO NOT INSTALL WITH `pip`!! This will not work.**
    -  If connecting remotely: Install the `ibm_db` package in any supported fashion. Db2 Connect licensing is required.

