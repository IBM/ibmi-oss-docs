# Guide to migrating from 5733-OPS to RPMs

## Environment setup (PATH)

By default, the RPM-form packages do not create symbolic links in standard,
used-by-default directories like `/QOpenSys/usr/bin/` or `/usr/bin/`.

There are two ways to address this:

1. (recommended) [Set the PATH environment variable](SETTING_PATH.md) so that
your shell will find the new commands when you try to run them.
2. (not recommended) Create symbolic links yourself in the `/QOpenSys/usr/bin`
directory for the tools you need to know. Most of the RPM-form deliverables will
ship the executables in the `/QOpenSys/pkgs/bin/` directory.

## Modifying scripts to use an appropriate "shebang" (#!) line

When writing a shell script (or a Python/Node.js program), it is common practice
to start your source code with a "shebang" line(`#!`). This tells the shell what
program to use when the script is run.

To properly use RPM-form executables, there are two options for making sure the
scripts use the RPM form, and not 5733-OPS.

The first (and most industry-standard) technique is to use the special
`/usr/bin/env` command in the shebang line, followed by the program that is
interpreting the script. This will look in your PATH for the named executable.
Thus, it is very important that your PATH be set correctly!!! For instance, for
a bash script:

``` bash
#!/usr/bin/env bash
echo "starting my shell script"
```

Another approach is to fully-qualify the path to the binary in
`/QOpenSys/pkgs/bin`. For instance:

``` bash
#!/QOpenSys/pkgs/bin/bash
echo "starting my shell script"
```

These techniques can apply to more than just shell scripts, and can be used for
other interpreted languages such as perl or Python. For example, here's how the
shebang line would look for a Python 3 program with the `/usr/bin/env` method

``` python3
#!/usr/bin/env python3
print("starting my python program")
```

And with the fully-qualified technique:

``` python3
#!/QOpenSys/pkgs/bin/python3
print("starting my python program")
```

## Python migration notes

- Rather than invoking `python`, invoke `python2` or `python3` depending on
which version of Python you are using. This also applies to other Python
commands. For instance, use `pip2` or `pip3` to invoke the Preferred Installer
for Python ("pip").
- Any globally-installed Python modules will need to be reinstalled (this is due
to the changing Python version)
- Whenever possible, Python packages should be globally installed via RPM
packages, rather than with the `pip` or `pip3` commands. See [this document](../PYTHON_PKGS_GUIDE.md)
for more information.
- Install the Db2 connection package with yum, by running
`yum install python3-ibm_db` or `yum install python2-ibm_db` (rather than
installing shipped .whl files)
- Install the itoolkit (XMLSERVICE interface) package with yum, by running
`yum install python3-itoolkit` or `yum install python2-itoolkit` (rather than
installing shipped .whl files)

## Node.js migration notes

See [Node.js usage notes](../node.js/README.md)
