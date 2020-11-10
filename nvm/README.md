# Node Version Manager

## Step 1: Install developer tools
From an SSH terminal, run:
```
yum group install "Development Tools"
```
## Step 2: Install NVM

First, install necessary prerequisites using [yum](../yum/) to verify that you have curl and/or wget installed. Make sure you [set your PATH](../troubleshooting/SETTING_PATH.md) to utilize the new open source technology.

Then, simply follow the installation steps on the [nvm project page](https://github.com/creationix/nvm/)

## Step 3: Configure your $HOME/.nvmrc file
Create a file at `$HOME/.nvmrc`, with the following contents
```
--dest-cpu=ppc64
--without-snapshot
--shared-openssl
--without-perfctr
```

## Step 4: Set necessary environment variables
Set the following environment variables:
```
OBJECT_MODE=64
CC=gcc
CXX=g++
```

Preferrably, set these in your `$HOME/.profile` and/or `$HOME/.bash_profile` (depending on your shell settings), by adding the following lines:
```
OBJECT_MODE=64
export OBJECT_MODE
CC=gcc
export CC
CXX=g++
export CXX
```

## Step 5: Run nvm!
NVM, like many open source commands, are best run from an SSH terminal. See the [nvm project page](https://github.com/creationix/nvm/) for example usages of the command. Some examples include:

* `nvm install stable` : install the latest stable version
* `nvm install --lts` : install the latest LTS release
* `nvm use --lts` : use the latest LTS release
