[TOC]

# RPM pile for IBM i 7.2+ (General Information)
Much of the open source technology available in the 5733-OPS product is now available in RPM form! This allows for a more seamless experience for those needing to install, manage, or use open source technologies. You can use the "yum" package manager to see the entire list of what packages are available.

**Some notable deliveries include:**

- Node.js version 8 
- Python 3.6
- The 'less' utility
- Git
- The 'updatedb' and 'locate' utilities (in the 'findutils' package)
- GCC 6.3.0 and many development tools such as automake, autoconf, m4, libtool, etc.
- GNU versions of many common utilities such as ls, grep, sed, awk.....
- GNU Nano
- many, many more things.....

# Getting Started
**There are two parts of this offering:**

- Install bootstrap tarball (bootstrap.tar.Z)
- Install from RPM repository

You will need to first install the bootstrap. Installing the "bootstrap" is a one-time process! This will install yum, RPM, their dependencies as well as a few other bits of software. The download repository will have further software that you can install.

Also, don't forget to read the Usage notes below. They are very important!

### Installing with Access Client Solutions (ACS)
- Download the latest release of Access Client Solutions

- Access the Open Source Package Management Interface through the "Tools" Menu of ACS

- For more information, see [this Technote](http://www-01.ibm.com/support/docview.wss?uid=nas8N1022619)

### Online Install Instructions (without ACS)
- Download [bootstrap.sql](ftp://public.dhe.ibm.com/software/ibmi/products/pase/rpms/bootstrap.sql) to your PC

- Open ACS Run SQL Scripts and connect to the IBM i you want to install to

- Open bootstrap.sql in your Run SQL Scripts window

- Execute "Run All" via Toolbar, Menu option, or Ctrl-Shift-A

- If the result is "Bootstrapping Successful" you're all good. If not, consult /tmp/bootstrap.log.

### Offline Install Instructions (without ACS)
- Download [bootstrap.sh](ftp://public.dhe.ibm.com/software/ibmi/products/pase/rpms/bootstrap.sh) and [bootstrap.tar.Z](ftp://public.dhe.ibm.com/software/ibmi/products/pase/rpms/bootstrap.tar.Z) to your PC

- Transfer these two files to the `/tmp` directory on your IBM i system (via FTP, mapped network drive, scp, etc�). Make sure to transfer them in binary.

- From a 5250 terminal run the following.

```
    QSH CMD('touch -C 819 /tmp/bootstrap.log; /QOpenSys/usr/bin/ksh /tmp/bootstrap.sh > /tmp/bootstrap.log 2>&1')
```

   - If you see message QSH005: "Command ended normally with exit status 0" in the job log you're all good. If not, consult `/tmp/bootstrap.log`.

   - If FTP is blocked by a firewall between the IBM i and the IBM FTP Server, you will have to perform the following in the /QOpenSys/etc/yum/repos.d/ directory: 

      1. Download the entire directory at ftp://public.dhe.ibm.com/software/ibmi/products/pase/rpms/repo 
      2. Upload the entire directory to IBM i ifs (EX: Upload it to /QOpenSys/etc/yum/IBMRepoLocalMirror/repo)
      3. Edit `ibm.repo` to add the following line to the "ibm" repository definition. This will prevent failure if/when your system can't talk to the IBM FTP Server:
 
          skip_if_unavailable=1
 

      4. Copy `ibm.repo` to a new file, with a .repo name (for instance, myrepo.repo)
      5. In the new .repo file, delete the skip_if_unavailable line, and change the baseurl to point to the local filesystem. This will make yum look on the IFS for the programs to install instead of trying to go to the IBM FTP serverThi: 
      
               FROM: baseurl=ftp://public.dhe.ibm.com/software/ibmi/products/pase/rpms/repo
               TO: baseurl=file:///path/to/local/repo
               EXAMPLE TO: baseurl=file:///QOpenSys/etc/yum/IBMRepoLocalMirror/repo



# Must-know Usage Notes!!! (READ THIS AFTER YOU INSTALL)
All software provided by the RPMs will install in to the `/QOpenSys/pkgs` prefix. You can fully qualify the path to the program or you can add `/QOpenSys/pkgs/bin` to your `PATH` to use the software. There are currently no plans to add symlinks in to `/QOpenSys/usr/bin` or `/QOpenSys/usr/lib`, though you can certainly do so if you like.

**Fully Qualifying:**

```
$ /QOpenSys/pkgs/bin/bash --version
GNU bash, version 4.4.12(1)-release (powerpc-ibm-os400)
Copyright (C) 2016 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>

This is free software; you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
```



**Adjusting your PATH:**

```
$ PATH=/QOpenSys/pkgs/bin:$PATH
$ export PATH

$ bash --version
GNU bash, version 4.4.12(1)-release (powerpc-ibm-os400)
Copyright (C) 2016 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>

This is free software; you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
```

If you want to make your `PATH` setting permanent, add the above line to your `$HOME/.profile`. You can do this easily (from a shell) like so.

```
echo 'PATH=/QOpenSys/pkgs/bin:$PATH' >> $HOME/.profile
export PATH >> $HOME/.profile
```


## Installing additional software
You no longer need to download all the rpms from the FTP to install them, as yum will do that for you.

**Using Access Client Solutions (ACS)**
[This Technote](http://www-01.ibm.com/support/docview.wss?uid=nas8N1022619) demonstrates how to use ACS to perform simple package management tasks such as adding, removing, or upgrading software.

**Yum cheat sheet**

If you don't know how to use yum, Red Hat has a handy "cheat sheet" available [here](https://access.redhat.com/sites/default/files/attachments/rh_yum_cheatsheet_1214_jcs_print-1.pdf).

**Common commands:**

- Install a package: `yum install <package>`
- Remove a package: `yum remove <package>`
- Search for a package: `yum search <package>`
- List installed packages: `yum list installed`
- List available packages: `yum list available`
- List all packages: `yum list all`

**Install python 3 and some useful Python packages:**

```
yum install python3 python3-ibm_db python3-itoolkit python3-pip python3-setuptools python3-six python3-wheel
```

**Install Node.js:**

```
yum install nodejs8 && nodever 8
```

**Install gcc:**

```
yum install gcc-aix libstdcplusplus-devel
```

**Using a chroot:**

If you'd like to install in to a chroot, you can use the scripts from [ibmichroot](https://bitbucket.org/litmis/ibmichroot) to set up a chroot using the `chroot_minimal.lst` and extract the bootstrap to there.

If you install to the root of the OS, you can use rpm to help install chroots. Use the `chroot_minimal.lst` to set up the chroot and then use the `--installroot` option on rpm to install the rpm in to that chroot.

```
yum --installroot=<path too chroot> install <package list>
```

The following dummy packages exist to satisfy RPM dependencies inside the chroot.

```
pase-libs-dummy-7.1-0.ibmi7.1.fat.rpm
coreutils-pase-dummy-7.1-0.ibmi7.1.ppc.rpm
```
 
# FAQ

## Is 5733-OPS required in order to install the RPM-based deliverables?

No. 5733-OPS does not need to be installed.

## When will tools and language runtimes be 64-bit enabled?

Most of the software available in RPM form is 64-bit, including the Python and Node.js runtimes


## Will 5733-OPS be updated to ship Node.js version 8, Python 3.6, or other goodies that are currently in RPM form only?

There are currently no plans to deliver these packages in the 5733-OPS installable product. If you have a business need for such, please submit an RFE with your justification.


## Is this the same thing as Perzl.org or other RPM's I have heard of (or used) in the past?

No. These RPM's are not AIX RPM's. They are IBM i RPMs shipping IBM i software. Built on IBM i, for IBM i.

## What if I am on IBM i 7.1?

With the exception of a handful of packages (including Node.js), much of the software will still work, but IBM i 7.2+ is the targeted release. Packages that are delivered for IBM i 7.1 may be rebuilt to only support IBM i 7.2+ without notice.



# Third-party (non-IBM) repositories
Information on third-party repositories can be found [here](3RD_PARTY_REPOS.md).