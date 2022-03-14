# Adjusting your PATH temporarily

```{toctree}
:maxdepth: 1
```

Temporarily adjust your path by running the following two commands:

```bash
PATH=/QOpenSys/pkgs/bin:$PATH
export PATH
```

After that, typing commands should find RPM-installed open source tools
(if using bash already, you may need to run `hash -r`, like the following example

```bash
$ bash --version
GNU bash, version 4.4.12(1)-release (powerpc-ibm-os400)
Copyright (C) 2016 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>

This is free software; you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
```

## HIGHLY Recommended: adjust your PATH permanently

If you want to make your `PATH` setting permanent, add the above line to your
`$HOME/.profile` and/or your `$HOME/.bash_profile` (if you are using bash).
You can do this easily (from a shell) like so.

```bash
touch $HOME/.profile
setccsid 1208 $HOME/.profile
echo 'PATH=/QOpenSys/pkgs/bin:$PATH' >> $HOME/.profile
echo 'export PATH' >> $HOME/.profile
```

To make this change for all users, put these lines in `/QOpenSys/etc/profile`,
like so:

```bash
touch /QOpenSys/etc/profile
setccsid 1208 /QOpenSys/etc/profile
echo 'PATH=/QOpenSys/pkgs/bin:$PATH' >> /QOpenSys/etc/profile
echo 'export PATH' >> /QOpenSys/etc/profile
```

**Need to run globally-installed Node.js modules,
or choose a Node.js version on a per-user basis?**

To run `node-gyp` or other globally-installed modules, or to switch the default
version of Node.js for a specific user, place `/QOpenSys/pkgs/lib/nodejs<version>/bin`
at the beginning of the user's PATH environment variable. For instance, that user
could run the following from the shell to set their default to version 10:

```bash
touch $HOME/.profile
setccsid 1208 $HOME/.profile
echo 'PATH=/QOpenSys/pkgs/lib/nodejs10/bin:/QOpenSys/pkgs/bin:$PATH' >> $HOME/.profile
echo 'export PATH' >> $HOME/.profile
```

(if using `bash` as the shell, the user may need to run `hash -r`)

## Verifying that your PATH is set correctly
Simply run the following from your operating environment:
```bash
echo $PATH
```
The output should be a `:`-delimited list of directories.
These will be searched, in order, for any commands entered
into your shell. The `PATH` should contain, at minimum,
`/QOpenSys/pkgs/bin`, very preferrably before the "standard"
paths like `/QOpenSys/usr/bin` or `/usr/bin`. You may also
see other PATHS you added to the beginning, for instance, 
to choose a Node.js version per the
[Node.js usage notes](../nodejs/README.md)

For example:
**Horrible**
```bash
/usr/bin:.:/QOpenSys/usr/bin
```

**Bad**
```bash
/QOpenSys/usr/bin:/usr/ccs/bin:/QOpenSys/usr/bin/X11:/usr/sbin:.:/usr/bin
```

**Marginal**
```bash
/QOpenSys/usr/bin:/usr/ccs/bin:/QOpenSys/usr/bin/X11:/usr/sbin:.:/usr/bin:/QOpenSys/pkgs/bin
```
**Best**
```bash
/QOpenSys/pkgs/bin:/QOpenSys/usr/bin:/usr/ccs/bin:/QOpenSys/usr/bin/X11:/usr/sbin:.:/usr/bin
```
