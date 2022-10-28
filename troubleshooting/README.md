# Common Open Source Problems (and how to fix them)

```{toctree}
:maxdepth: 1
```

## Things to always check first when troubleshooting

The first step in troubleshooting is to ensure that
all of the following are true:
- You are accessing the system with an SSH terminal
    - If you insist on using 5250, favor QP2TERM over
      QSH. If using QSH, ensure that the `QIBM_MULTI_THREADED`
      environment variable is set to `Y` **before**
      launching QSH
    - If you insist on using 5250, be aware that you
      are more likely to have problems, even if the
      above precautions are taken.
- You have your `PATH` environment variable set properly.
  See [Setting your PATH](SETTING_PATH.md) for guidance.
- You are only editing files with only ASCII or UTF8-based
  editors, such as:
    - (Recommended) A cross-platform editor such as VSCode,
      Notepad++, jEdit, etc.
    - an SSH terminal UI-based editor, such as vim, nano,
      or jmacs.
- You don't have CRLF line terminators in your files. This
  can happen if you have edited your file from Windows and
  do not have your editor properly configured. If you
  are unsure, install the `dos2unix` package and run
  the resulting `dos2unix` utility on your file.

## Shell cannot find yum command

When running the `yum` command from the command line, you encounter an error like:

- `-bash: yum: command not found`
- `yum: not found`
- `ksh: yum:  not found`
- `qsh: 001-0019 Error found searching for command yum. No such path or directory.`

**Solution:**

Add `/QOpenSys/pkgs/bin` to the beginning of your PATH environment variable. See
[Setting your PATH](SETTING_PATH.md) for details

Also, please don't use QSH for open source tools. Use an SSH terminal instead.

## yum connectivity issues

See [this doc](YUM.md)

## yum can't connect to the repository (with thread error)

When running yum from QSH, any commands that connect to the repository (install
upgrade, etc) fail with a message like so:

```sh
yum install python3
https://public.dhe.ibm.com/software/ibmi/products/pase/rpms/repo/repodata/repomd.xml: [Errno 14] curl#6 - "getaddrinfo() thread failed to start"
Trying other mirror.
Error: Cannot retrieve repository metadata (repomd.xml) for repository: ibm. Please verify its path and try again
```

**Solution:**

Run yum via SSH or the ACS Open Source Package Manager GUI. These are the ideal
interfaces for working with yum and the rest of the open source ecosystem.

If you need to work from 5250, QP2TERM is preferred over QSH, but QSH _will_
work as long as the `QIBM_MULTI_THREADED` environment variable is set to `Y` at
the job level.

## Up arrow doesn't recall previous commands

Using arrow keys in the shell causes "garbage" to be displayed on the screen
instead of cycling through command history (eg. `^[[A^[[D^[[C^[[C^[[D^[[A`)

**Solution:**

The default shell used by SSH is `bsh`, which is very primitive. You will
probably want to set `bash` as your default shell. See
[Setting bash as your shell](SETTING_BASH.md) for details.


## User input is not working properly when running in 5250

Generally speaking, **open source programs do not work well in 5250 interfaces**
such as QSH or Qp2Term. This may result in improper processing of control keys,
phantom user input from previous commands, "garbage" characters printed to the
screen, or a host of other issues. This strange behavior can affect `bash` or
any open source software. 

There may also be issues with process groups and job control. In particular,
attempts to run `bash` in a 5250 environment may result in an error similar to
the following:
```
bash: cannot set terminal process group (1319667): A system call received a parameter that is not valid.
bash: no job control in this shell                                                                      
```

**Solution:**

Please use an SSH terminal emulator and an SSH connection. Also, for usability,
you probably want to set `bash` as your default shell. See
[Setting bash as your shell](SETTING_BASH.md) for details.

## Python can't find packages installed from ACS

After installing a Python package from ACS (eg. `python3-Pillow`), it can't be found.

**Solution:**

- Ensure you are running the correct version of Python for the package that was
installed: `python3` for packages with the `python3` prefix and `python2` for
packages with the `python2` prefix.
- Also ensure that your `PATH` environment variable is set to find
`/QOpenSys/pkgs/bin` before `/QOpenSys/usr/bin` and `/usr/bin`, especially if
you potentially have other Pythons installed from 5733-OPS or Perzl rpms. See
[Setting your PATH](SETTING_PATH.md) for details.

*NOTE: neither `python` rpm installed via yum creates a `python` symlink, so you
cannot just run `python`.*

## Yum or RPM fails with "Error: Error: rpmdb open failed"

When Running a `yum` or `rpm` command you encounter

```text
Error: Error: rpmdb open failed
```

**Solution:**

The rpm database has gotten corrupted. Please report this issue [here](http://ibm.biz/ibmi-rpm-issue-tracker).

The common solution is to rebuild the database with

```sh
/QOpenSys/pkgs/bin/rpm --rebuilddb
```

## Yum or RPM fails with "db4 error(19) from dbenv->open: The specified device does not exist."

Running yum you encounter an error like

```text
error: db4 error(19) from dbenv->open: The specified device does not exist.
error: cannot open Packages index using db4 - The specified device does not exist. (19)
error: cannot open Packages database in /QOpenSys/var/lib/rpm
CRITICAL:yum.main:
Error: rpmdb open failed 
```

You probably have journalling on for an IFS directory that rpm is using. rpm
uses `mmap` to open its database files, which is incompatible with journaling.

*Note: When an ILE a application tries to `mmap` an IFS file which is being
journaled it gets an error - `ENOTSUP` (operation not supported), however this
gets mapped to PASE as `ENODEV` (no such device) which makes things confusing.*

**Solution:**

Ensure that journaling is disabled/omitted for `/QOpenSys/var/lib/rpm` or any
subdirectory. You can use option 8 from `WRKLNK` to view the journaling
attributes of a given file or directory.

## Commands are failing in QSH

Many commands will fail in QSH for many reasons! However, a common reason is related
to the QSH behavior that disallows multithreaded applications by default. The resulting
error message may or may not be descriptive, but here are some examples.

git:
```text
error: cannot create async thread: Resource temporarily unavailable
fatal: fetch-pack: unable to fork off sideband demultiplexer 
```

node/npm:
```text
[335708]: ../src/node_platform.cc:61:std::unique_ptr<unsigned int> node::Work   erThreadsTaskRunner::DelayedTaskScheduler::Start(): Assertion `(0) == (uv_thr   ead_create(t.get(), start_thread, this))' failed.
qsh: 001-0078 Process ended by signal 5.                                     
```

curl:
```text
curl: (6) getaddrinfo() thread failed to start 
```

java (openjdk):
```text
Error: Port Library failed to initialize: -1             
Error: Could not create the Java Virtual Machine.        
Error: A fatal exception has occurred. Program will exit.
```

**Solution:**

As mentioned earlier, the optimal solution is to connect with an SSH client.
If you insist on using 5250, favor QP2TERM over QSH. If using QSH,you must
ensure that the `QIBM_MULTI_THREADED` environment variable is set to `Y`
**before** launching QSH.
      
## Ansible fails with "No python interpreters found"

If running Ansible against an IBM i endpoint, it can sometimes fail with
the following warning issued:

```
[WARNING]: No python interpreters found for host __________ (tried ['/usr/bin/python', 'python3.7', 'python3.6', 'python3.5', 'python2.7', 'python2.6', '/usr/libexec/platform-python', '/usr/bin/python3', 'python'])
```

This is because Ansible does not currently know how to find the RPM-installed
Python interpreters on IBM i
(GitHub [issue](https://github.com/ansible/ansible/issues/77458) pending).

**Solution:** 

This can often be corrected by [fixing the PATH](./SETTING_PATH.md) of the user
that you are using to connect with Ansible. 

It's likely best, however, to be more explicit, so you're not as susceptible
to variations in server environments. To do so, you can set Ansible's
`ansible_python_interpreter` inventory variable to a fully-qualified path,
namely `/QOpenSys/pkgs/bin/python3.9` (use version 3.6 if absolutely needed).
This can be done in the various ways. See
[this doc](https://docs.ansible.com/ansible/latest/reference_appendices/python_3_support.html).

## Ansible (or another SSH-based tool) asks for a password

If you'd like to run Ansible (or similar SSH-based tools) non-interactively and
without a password, it can sometimes still ask for a user password (and
therefore fail in non-interactive environments). 

**Solution:** 

You need to configure password-less authentication per
[this doc](../user_setup/README.md), just use the same Linux and IBM i system
and user. Alternatively, once you install your public key on the IBM i server,
provide your private key to ansible by way of the
`ansible_ssh_private_key_file` inventory variable. More info
[here](https://docs.ansible.com/ansible/latest/user_guide/connection_details.html).
**Always make sure that your private key is kept secure!**

## "intended for a different operating system" when running IBM i 7.4
If you installed the open source "bootstrap" from a very early version, and have since
upgraded to IBM i 7.4, you may see errors like the following when trying to
install a package:

```fortran
Transaction Check Error:
  package make-gnu-4.2-2.ppc64 is intended for a different operating system
```

**Solution:** 

The very early versions of the bootstrap did not know IBM i 7.4 existed. You can work
around this issue by adding an OS compatibility setting to the RPM configuration,
as shown in the following command:

```bash
echo 'os_compat: ibmi7.4: ibmi ibmi7.1 ibmi7.2 ibmi7.3' >> /QOpenSys/pkgs/lib/rpm/rpmrc
```

It is then recommended to get the latest versions of `rpm`, `yum`, and `ibmi-repos`
packages:

```bash
/QOpenSys/pkgs/bin/yum install -y rpm yum ibmi-repos
```

## rsync from another system fails with `rsync: not found`

When using rsync from another operating system (Linux, for instance), rsync may be
unable to locate the `rsync` executable on IBM i and will therefore fail. The error
message may resemble something like this:

```fortran
bsh: rsync: not found
rsync: connection unexpectedly closed (0 bytes received so far) [sender]
rsync error: error in rsync protocol data stream (code 12) at io.c(228) [sender=3.2.3]
```

**Solution #1 (recommended):** 

Install the `rsync-compat` package on your IBM i system.

```fortran
/QOpenSys/pkgs/bin/yum install rsync-compat
```


**Solution #2 (adjust your PATH):** 

First, make sure that the `rsync` RPM package is installed on IBM i.
Ensure that the `PATH` environment variable is set to include the `/QOpenSys/pkgs/bin` path.
The most prescriptive technique for doing so is documented [here](SETTING_PATH.md). Note that
bash-specific approaches (use of .bash_profile, for instance) will not work if your default
shell is `bsh` or some other non-bash option.

**Solution #3 (explicitly set remote rsync path):**

First, make sure that the `rsync` RPM package is installed on IBM i.
When invoking the rsync command, use the following option on the command line:

```fortran
--rsync-path=/QOpenSys/pkgs/bin/rsync
```

For instance:
```fortran
rsync --rsync-path=/QOpenSys/pkgs/bin/rsync -a src user@ibmiserver:/path/to/destination
```

## I'm still having issues

If you are having an issue that's not listed above or the solution provided did
not help, please open a ticket [here](http://ibm.biz/ibmi-oss-issues).
