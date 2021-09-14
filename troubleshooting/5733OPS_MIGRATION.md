# Guide to migrating from 5733-OPS to RPMs

## Environment setup (PATH)

By default, the RPM-form packages do not create symbolic links in standard,
used-by-default directories like `/QOpenSys/usr/bin/` or `/usr/bin/`.

To address this, [Set the PATH environment variable](SETTING_PATH.md) so that
your shell will find the new commands when you try to run them.
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
shebang line would look for a `python3.9` program with the `/usr/bin/env` method

``` python3
#!/usr/bin/env python3.9
print("starting my python program")
```

And with the fully-qualified technique:

``` python3
#!/QOpenSys/pkgs/bin/python3.9
print("starting my python program")
```

## Python migration notes

See [Python usage notes](../python/README.md)

## Node.js migration notes

See [Node.js usage notes](../node.js/README.md)
