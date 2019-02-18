# Common Open Source Problems (and how to fix them)

Problem  | Fix
------------- | -------------
qsh: 001-0019 Error found searching for command yum.  | Please use an SSH terminal to access open source tools. 
yum: command not found | Add `/QOpenSys/pkgs/bin` to the beginning of your PATH environment variable. See [Setting your PATH](SETTING_PATH.md) for details
Up arrow doesn't recall previous commands | You will want to install `bash` and set it as your default shell. See [Setting bash as your shell](SETTING_BASH.md) for details
After I install a python module with ACS, Python still can't find it | Make sure you are running `python3` if you are using a Python 3 module. Also, ensure you are not running the OPS Python, which will not see the package. Running `which python3` or `which python2` should show you which one you are using. Binaries from RPM packages will exist in `/QOpenSys/pkgs/bin`. A recommendation would be to add `/QOpenSys/pkgs/bin` to the beginning of your PATH environment variable. See [Setting your PATH](SETTING_PATH.md) for details. Also, reinstalling the package from ACS will help if you have used the `pip` or `pip3` commands to remove the module.
Yum or RPM fails with "Error: Error: rpmdb open failed" | The RPM database has gotten corrupted (please report this in the issues with any info about what preceding actions where). First, ensure that jornaling is disabled for `/QOpenSys/var/lib/rpm directory` structure (or any parent directory). Next rebuild the database by running `/QOpenSys/pkgs/bin/rpm --rebuilddb`
