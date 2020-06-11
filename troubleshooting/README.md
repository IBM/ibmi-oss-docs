# Common Open Source Problems (and how to fix them)

## Shell cannot find yum command

### Problem

When running the `yum` command from the command line, you encounter an error like:

- `-bash: yum: command not found`
- `yum: not found`
- `ksh: yum:  not found`
- `qsh: 001-0019 Error found searching for command yum. No such path or directory.`

### Solution

Add `/QOpenSys/pkgs/bin` to the beginning of your PATH environment variable. See [Setting your PATH](SETTING_PATH.md) for details

Also, please don't use QSH for open source tools. Use an SSH terminal instead.

## yum can't connect to the repository

### Problem

When running yum from QSH, any commands that connect to the repository (install upgrade, etc) fail with a message like so:

```
yum install python3
https://public.dhe.ibm.com/software/ibmi/products/pase/rpms/repo/repodata/repomd.xml: [Errno 14] curl#6 - "getaddrinfo() thread failed to start
"
Trying other mirror.
Errore: Cannot retrieve repository metadata (repomd.xml) for repository: ibm. Please verify its path and try again
```

### Solution

Run yum via SSH or the ACS Open Source Package Manager GUI. These are the ideal interfaces for working with yum and the rest of the open source ecosystem.

If you need to work from 5250, QP2TERM is preferred over QSH, but QSH _will_ work as long as the `QIBM_MULTI_THREADED` environment variable is set to `Y` at the job level.

## Up arrow doesn't recall previous commands

### Problem

Using arrow keys in the shell causes "garbage" to be displayed on the screen instead of cycling through command history (eg. `^[[A^[[D^[[C^[[C^[[D^[[A`)

### Solution

The default shell used by SSH is `bsh`, which is very primitive. You will probably want to set `bash` as your default shell. See [Setting bash as your shell](SETTING_BASH.md) for details.

## Python can't find packages installed from ACS

### Problem

After installing a Python package from ACS (eg. `python3-Pillow`), it can't be found.

### Solution

- Ensure you are running the correct version of Python for the package that was installed: `python3` for packages with the `python3` prefix and `python2` for packages with the `python2` prefix. 
- Also ensure that your `PATH` environment variable is set to find `/QOpenSys/pkgs/bin` before `/QOpenSys/usr/bin` and `/usr/bin`, especially if you potentially have other Pythons installed from 5733-OPS or Perzl rpms. See [Setting your PATH](SETTING_PATH.md) for details.

*NOTE: neither `python` rpm installed via yum creates a `python` symlink, so you cannot just run `python`.*


## Yum or RPM fails with "Error: Error: rpmdb open failed"

### Problem

When Running a `yum` or `rpm` command you encounter

```text
Error: Error: rpmdb open failed
```

### Solution

The rpm database has gotten corrupted. Please report this issue [here](http://ibm.biz/ibmi-rpm-issue-tracker).

The common solution is to rebuild the database with

```sh
/QOpenSys/pkgs/bin/rpm --rebuilddb
```

## Yum or RPM fails with "db4 error(19) from dbenv->open: The specified device does not exist."


### Problem

Running yum you encounter an error like

```text
error: db4 error(19) from dbenv->open: The specified device does not exist.
error: cannot open Packages index using db4 - The specified device does not exist. (19)
error: cannot open Packages database in /QOpenSys/var/lib/rpm
CRITICAL:yum.main:
Error: rpmdb open failed 
```

You probably have journalling on for an IFS directory that rpm is using. rpm uses `mmap` to open its database files, which is incompatible with journalling.

*Note: When an ILE a application tries to `mmap` an IFS file which is being journalled it gets an error - `ENOTSUP` (operation not supported), however this gets mapped to PASE as `ENODEV` (no such device) which makes things confusing.*

### Soution

Ensure that journalling is disabled/omitted for `/QOpenSys/var/lib/rpm` or any subdirectory. You can use option 8 from `WRKLNK` to view the journalling attributes of a given file or directory.

## I'm still having issues!

If you are having an issue that's not listed above or the solution provided did not help, please open a ticket [here](https://bitbucket.org/ibmi/opensource/issues).
