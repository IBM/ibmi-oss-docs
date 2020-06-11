[TOC]

# RPM pile for IBM i releases in standard support

## General Information

Much of the open source technology available in the 5733-OPS product is now available in RPM form! This allows for a more seamless experience for those needing to install, manage, or use open source technologies. You can use the "yum" package manager to see the entire list of what packages are available.

### Notable deliverables

- Node.js version 8 and version 10
- Python 3.6
- The 'less' utility
- git
- The 'updatedb' and 'locate' utilities (in the 'findutils' package)
- GCC 6.3.0 and many development tools such as automake, autoconf, m4, libtool, etc.
- GNU versions of many common utilities such as ls, grep, sed, awk.....
- GNU Nano
- many, many more things.....

## Installation

Once you have `yum` installed, you can install, remove, and upgrade rpms easily. `yum` is even able to update and install new versions of itself! But how do you install `yum` if you don't have `yum` installed? We have a Catch-22! To get around this loop, we have provided a bootstrap installer which installs and configures yum via a different mechanism which has just enough to get `yum` and installed and working. As said before, once `yum` is installed it can update itself, so this bootstrap process is only needed once!

*NOTE: Don't forget to read the Usage Notes below. They are very important!*

### Installing with Access Client Solutions (ACS)

*NOTE: This currently requires that your PC have direct HTTPS access to the public IBM file server. If for some reason, you cannot access external sites via HTTPS, refer to steps in "Offline Install Instructions (without ACS)".*

*You will also need SSH connectivity from your PC to the IBM i system. Be sure to have the SSH daemon running on IBM i (`STRTCPSVR *SSHD`).*

*This technique does not require external Internet access from your IBM i system..*

- Download the latest release of Access Client Solutions

- Access the Open Source Package Management Interface through the "Tools" Menu of ACS

- For more information, see [this Technote](http://www-01.ibm.com/support/docview.wss?uid=nas8N1022619)

### Online Install Instructions (without ACS Open Source Management Tool)

*NOTE: This requires that your IBM i have direct FTP access to the public IBM file server from your IBM i system. Many companies now block FTP access. If that is the case, refer to steps in "Offline Install Instructions (without ACS)".*

- Download [bootstrap.sql](https://public.dhe.ibm.com/software/ibmi/products/pase/rpms/bootstrap.sql) to your PC

- Open ACS Run SQL Scripts and connect to the IBM i you want to install to

- Open bootstrap.sql in your Run SQL Scripts window

- Execute "Run All" via Toolbar, Menu option, or Ctrl-Shift-A

- If the result is "Bootstrapping Successful" you're all good. If not, consult /tmp/bootstrap.log.

### Offline Install Instructions (without ACS)

- Download [bootstrap.sh](https://public.dhe.ibm.com/software/ibmi/products/pase/rpms/bootstrap.sh) and [bootstrap.tar.Z](https://public.dhe.ibm.com/software/ibmi/products/pase/rpms/bootstrap.tar.Z) to your PC

- Transfer these two files to the `/tmp` directory on your IBM i system (via FTP, mapped network drive, scp, etc). *Make sure to transfer them in binary.*

- From a 5250 terminal run the following.

```text
    QSH CMD('touch -C 819 /tmp/bootstrap.log; /QOpenSys/usr/bin/ksh /tmp/bootstrap.sh > /tmp/bootstrap.log 2>&1')
```

- If you see message QSH005: "Command ended normally with exit status 0" in the job log you're all good. If not, consult `/tmp/bootstrap.log`.

## Switching from FTP to HTTP(S)

The original bootstrap used FTP to connect to the public IBM file server. This server has now had HTTP and HTTPS enabled, so you can switch to using HTTP if you prefer. This is especially useful if your corporate firewall rules disallow unsecured FTP (which many do).

The easiest way to do so is to download the new [repo file](https://public.dhe.ibm.com/software/ibmi/products/pase/rpms/ibm.repo) and replace the one at `/QOpenSys/etc/yum/repos.d/ibm.repo`. There are numerous ways to do this, but perhaps the easiest is with `curl`:

```bash
curl http://public.dhe.ibm.com/software/ibmi/products/pase/rpms/ibm.repo > /QOpenSys/etc/yum/repos.d/ibm.repo
```

*NOTE: If you download it another way, make sure to transfer it to the IBM i system in binary or ASCII modes.*


## Using yum on an IBM i system without internet access

If your IBM i system does not have access to the internet, yum will not be able to connect to the public IBM file server to download rpms. There are a number of options to overcome this limitation:

### 1. Use a proxy

If you have a proxy server available to you on your local intranet, yum can be configured to use it. Under the `main` section in `/QOpenSys/etc/yum/yum.conf` you can set `proxy`, `proxy_username`, and `proxy_password` options. eg.

```ini
[main]
proxy=http://proxy.mycompany.example.com:1234
proxy_username=user_name
proxy_password=passw0rd
```

### 2. Create a local repository mirror

If you want to keep a local cache of the repository, you can use the `reposync` and `createrepo` commands to create a complete copy of the remote repo. You'll need to do this from a system which does have external (outbound) network access. It can be on any OS which has the above tools available (on IBM i `yum install yum-utils createrepo` to install them).

```shell
reposync -p /path/to/repo/root -r ibm
createrepo /path/to/repo/root/ibm
```

If you are running this from a non-IBM i system, you will need to run the `reposync` command twice, specifying different `-a` parameters to download all the different architecture packages, eg.

```shell
reposync -a ppc64 -p /path/to/repo/root -r ibm
reposync -a fat   -p /path/to/repo/root -r ibm
createrepo /path/to/repo/root/ibm
```

Once this is done, you can share `/path/to/repo/root/ibm` on your local network using an HTTP server. This will be your new IBM i repository URL, so change the URL in the `ibm.repo` file to match.

Now that you are downloading the files through a mirror, you will need to keep the mirror in sync. Setting up a periodic task (via scheduled job or `cron`) to run the above commands will make this easy, but you can also do it manually as well.

## Must-know Usage Notes!!! (READ THIS AFTER YOU INSTALL)

All software provided by the RPMs will install in to the `/QOpenSys/pkgs` prefix. You can fully qualify the path to the program or you can add `/QOpenSys/pkgs/bin` to your `PATH` to use the software. There are currently no plans to add symlinks in to `/QOpenSys/usr/bin` or `/QOpenSys/usr/lib`, though you can certainly do so if you like.

### Fully Qualifying

```sh
/QOpenSys/pkgs/bin/bash --version
GNU bash, version 4.4.12(1)-release (powerpc-ibm-os400)
Copyright (C) 2016 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>

This is free software; you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
```

### Adjusting your PATH

```sh
PATH=/QOpenSys/pkgs/bin:$PATH
export PATH

bash --version
GNU bash, version 4.4.12(1)-release (powerpc-ibm-os400)
Copyright (C) 2016 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>

This is free software; you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
```

If you want to make your `PATH` setting permanent, add the above line to your `$HOME/.profile`. You can do this easily (from a shell) like so.

```sh
echo 'PATH=/QOpenSys/pkgs/bin:$PATH' >> $HOME/.profile
echo 'export PATH' >> $HOME/.profile
```

## Installing additional software

### Using Access Client Solutions (ACS)

[This Technote](http://www-01.ibm.com/support/docview.wss?uid=nas8N1022619) demonstrates how to use ACS to perform simple package management tasks such as adding, removing, or upgrading software.

### Yum cheat sheet

If you don't know how to use yum, Red Hat has a handy "cheat sheet" available [here](https://access.redhat.com/sites/default/files/attachments/rh_yum_cheatsheet_1214_jcs_print-1.pdf).

### Common commands

- Install a package: `yum install <package>`
- Remove a package: `yum remove <package>`
- Search for a package: `yum search <package>`
- List installed packages: `yum list installed`
- List available packages: `yum list available`
- List all packages: `yum list all`

### Installing Python 3 and some useful Python packages

```shell
yum install python3-pip python3-ibm_db python3-itoolkit
```

### Installing Python 3 Machine Learning packages

```shell
yum install python3-numpy python3-pandas python3-scikit-learn python3-scipy
```

### Installing Node.js

```sh
yum install nodejs10
```

### Installing GCC and development tools

```sh
yum group install "Development tools"
```

### Using a chroot

If you'd like to install in to a chroot, you can use the scripts from [ibmichroot](https://bitbucket.org/litmis/ibmichroot) to set up a chroot using the `chroot_minimal.lst` and extract the bootstrap to there.

If you install to the root of the OS, you can use rpm to help install chroots. Use the `chroot_minimal.lst` to set up the chroot and then use the `--installroot` option on rpm to install the rpm in to that chroot.

```sh
yum --installroot=<path too chroot> install <package list>
```

The following dummy packages exist to satisfy RPM dependencies inside the chroot.

```sh
pase-libs-dummy-7.1-0.ibmi7.1.fat.rpm
coreutils-pase-dummy-7.1-0.ibmi7.1.ppc.rpm
```

## Troubleshooting

Having issues? Please check out the [troubleshooting guide](../troubleshooting/).

## FAQ

### What if I run in to issues?

See **Troubleshooting** section above.

### How do I get support for open source on IBM i?

Open source support is available through community channels or an IBM premium support offering. See http://ibm.biz/ibmi-oss-support

### Is 5733-OPS required in order to install the RPM-based deliverables?

No. 5733-OPS does not need to be installed.

### When will tools and language runtimes be 64-bit enabled?

Most of the software available in RPM form is 64-bit, including the Python and Node.js runtimes

### Will 5733-OPS be updated to ship Node.js version 8, Python 3.6, or other goodies that are currently in RPM form only?

There are currently no plans to deliver these packages in the 5733-OPS installable product. If you have a business need for such, please submit an RFE with your justification.

### Is this the same thing as Perzl.org or other RPM's I have heard of (or used) in the past?

No. These RPM's are not AIX RPM's. They are IBM i RPMs shipping IBM i software. Built on IBM i, for IBM i.

### What if I am on an IBM i release no longer in standard support?

IBM strives to provide community open source software packages for IBM i releases in standard support. Packages (including the initial installer) that are delivered for any IBM i release no longer in standard support may be rebuilt without notice, in an effort to leverage the latest technology for IBM i customers.

### Third-party (non-IBM) repositories

Information on third-party repositories can be found [here](3RD_PARTY_REPOS.md).
