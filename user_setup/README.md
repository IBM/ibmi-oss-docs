# Setting up a User's Environment

As referenced in [our troubleshooting guide](../troubleshooting/README.md)
and throughout this document, the recommended way to access
most open source tools is by way of using an SSH terminal. 
[This blog entry](https://techchannel.com/SMB/08/2017/embrace-ssh),
although a bit dated, summarizes some of the benefits. 

**It is not recommended to use a 5250 interface for running open source
tools!**

This document intends to walk you through the process of initializing
environment to use SSH efficiently.

This document also assumes your system administrator has installed the
open source toolset on IBM i as documented [here](../yum/README.md).

```{toctree}
:maxdepth: 1
```

## Step 1: Install an SSH client

There are many free SSH terminal emulators on the market. For the most part,
any of these choices will serve you well. Here is a non-exhaustive list
of options:

For Windows users:
 - PuTTY
 - Windows Subsystem for Linux (WSL)
 - git bash
 - Cygwin (ensure the "openssh" package is selected during installation)

For Mac/Linux users, the "ssh" command is often already installed. To verify,
just open up a terminal window and run:

```bash
ssh --version
```

## Step 2: Create your first connection to the system

If using one of the other options, your steps are generally to first open up
a terminal window.
On Windows, this varies based on which tool you are using. For instance:
- WSL: press `<windows_key>+r` and type `bash`
- git bash: press `<windows_key>` and search apps for `git bash`
- Cygwin: press `<windows_key>` and search apps for `Cygwin64 Terminal`
- PuTTY: See [these steps (external link)]([PUTTY_CONFIGURE_CONNECTION.md](https://cuit.columbia.edu/putty)) for more info.

Once a terminal window is open, connect to the IBM i system with the following
command:

```ssh
ssh user@system
```

(Of course, replace `user` with your user profile, and `system` with the host
name or IP address of your IBM i system)

Enter your password as requested. You should now be connected!

**Gotcha!!**

If your IBM i user profile is longer than 8 characters long, and you are
running IBM i 7.3 or earlier, you need to remove this restriction by way 
of the `PASE_USRGRP_LIMITED` environment variable. The easy way to do this
is to have your system administrator set it system-wide:

```lisp
ADDENVVAR ENVVAR(PASE_USRGRP_LIMITED) VALUE('N') LEVEL(*SYS)
```

## Step 3: Create your home directory

From your SSH session, run the following command:

```bash
mkdir -p $HOME
```

Now, verify this was successful by running the following commands:

```bash
cd $HOME
pwd
```

The output of the `pwd` command should match your home directory as configured
in your IBM i user profile (typically `/home/USRPRF`).

## Step 4: Change your default shell to `bash`

The default shell program on IBM i is very deficient as an operating environment.
It is highly recommended that you use bash by following
[these steps](../troubleshooting/SETTING_BASH.md), which essentially boils down to
running this command in your SSH session:

```bash
/QOpenSys/pkgs/bin/chsh -s /QOpenSys/pkgs/bin/bash
```

(there is also an SQL approach in the docs, if that is preferred)

When complete, exit your SSH session by typing `exit` and reconnecting as you did
earlier. You should now be running bash, as evidenced by a command prompt that
indicates a bash version (for instance, `-bash-5.1`).

## Step 5: Configure your `PATH`

In order for your woking environment to find the open source toolset, you need
to set up your `PATH` (environment variable) appropriately. The `PATH` is
often considered analogous to a library list. Instead of libraries, though,
it contains a list of directories to be searched for UNIX-style commands, as
would be run in a PASE environment (SSH) on IBM i. 

Configuration of `PATH` is documented in
[these steps](../troubleshooting/SETTING_PATH.md), which boils down to
running this sequence of commands in your SSH session:

```bash
touch $HOME/.profile
setccsid 1208 $HOME/.profile
echo 'PATH=/QOpenSys/pkgs/bin:$PATH' >> $HOME/.profile
echo 'export PATH' >> $HOME/.profile
```

When complete, exit your SSH session by typing `exit` and reconnecting as you did
earlier. Your environment should now have `PATH` set up properly. To verify this, 
run the following command:

```bash
which bash
```

Output should be:

```matlab
/QOpenSys/pkgs/bin/bash
```

## Step 6 (optional): Configure password-less login

Would you like to `ssh` into a system without typing your password? If so,
you can use a public/private key pair to authenticate to the system. 

### Step 6a: Generate a key pair

The first thing you need to do is generate a key pair. PuTTY ships a "PuTTYgen"
utility to do this. For other clients, run the following command from your
terminal, and respond appropriately to any questions it asks:

```
ssh-keygen
```

**IMPORTANT NOTE**: A key pair consists of a public key and a private key.
Never, under **any** circumstances, share your private key with another
entity. It should exist on your local system only. 

### Step 6b: copy public key to server

Next, you can copy your public key to the IBM i server by running the following
command from your terminal:

```bash
ssh-copy-id user@host
```

If, for some reason you don't have the `ssh-copy-id` command, or if you used
PuTTYgen to generate your key pair, you can manually copy the key to the server.
To do so, you can first create the server-side file by running the following:

```
mkdir -p $HOME/.ssh
touch $HOME/.ssh/authorized_keys
```

The `authorized_keys` file will store your public keys for any clients wishing
to connect with key-based authentication. After this file is created, you can
add your public key. To do so, locate the file on your PC with the public key.
This is usually stored in a file named "id_algorithm.pub", where "algorithm"
is the key pair algorithm. Most commonly, the file name is `id_rsa.pub`. If
using PuTTYgen, the user interface shows a text field labeled "public key
for pasting into OpenSSH authorized_keys file:". You can copy/paste that into
a file for use with the next step.

Once you've located your public key file, you can place it into your home
directory on IBM i, open an SSH session and run (substitute file name
as needed, this example assumes `id_rsa.pub`):

```bash
cat id_rsa.pub >> $HOME/.ssh/authorized_keys
rm id_rsa.pub
```

### Step 6c: Fix filesystem permissions

OpenSSH strictly enforces that the permissions of the necessary directories
and files are set in a secure manner. It will not work unless the permissions
are set correctly. To fix them up, run the following commands in your SSH
terminal:

```bash
chown "$(/QOpenSys/usr/bin/id -u -n)" $HOME
chown -R "$(/QOpenSys/usr/bin/id -u -n)" $HOME/.ssh
chmod 0755 $HOME
chmod 0700 $HOME/.ssh
chmod 0644 $HOME/.ssh/authorized_keys
```

### Step 6d: Verify password-less login

Sign out of your SSH session. Sign on again, as you did before (for instance,
`ssh user@host`). You should now be able to log in without a password!

## Having problems?

If you're having any problems, feel free to reach out to the various community
and support resources listed in [the IBM i Open Source resources](http://ibm.biz/ibmioss).

## Want an even more robust experience?

Check out [the dotfiles project](https://github.com/jbh/ibmi-dotfiles), which
provides more advanced environment customizations for the IBM i. This is especially
useful for Linux users on IBM i.
