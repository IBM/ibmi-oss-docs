# Adjusting your PATH temporarily
Termporarily adjust your path by running the following two commands:
```
PATH=/QOpenSys/pkgs/bin:$PATH
export PATH
```
After that, typing commands should find RPM-installed open source tools (if using bash already, you may need to run `hash -r`, like the following example
```
$ bash --version
GNU bash, version 4.4.12(1)-release (powerpc-ibm-os400)
Copyright (C) 2016 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>

This is free software; you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
```

# HIGHLY Recommended: adjust your PATH permanently
If you want to make your `PATH` setting permanent, add the above line to your `$HOME/.profile` and/or your `$HOME/.bash_profile`. You can do this easily (from a shell) like so.

```
echo 'PATH=/QOpenSys/pkgs/bin:$PATH' >> $HOME/.profile
export PATH >> $HOME/.profile
```