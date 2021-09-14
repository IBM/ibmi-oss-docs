# Node.js usage notes
All things assume you have [PATH set correctly](../troubleshooting/SETTING_PATH.md)

## Choosing which major version of Node.js to use
There are two ways to install Node.js:
1. Through the [package manager](https://nodejs.org/en/download/package-manager/#ibm-i) (recommended for production. Note that there are different packages for different major versions. A simple `yum upgrade` will not upgrade any existing versions to a new major version. 
2. Using [nvm](#using-node-version-manager-nvm)

Consult the [Node.js release schedule](https://github.com/nodejs/Release) for guidance on which version of Node.js to use. Generally speaking:
- Only even-numbered major releases should be deployed to production. The odd-numbered releases are feature releases designed to allow early access to new features. Feature releases lack both stability and a long-term support (LTS) schedule
- Choose a version that is in "Active LTS" status for production applications. "Current" status is sometimes acceptable as well, as long as the release will be entering LTS soon. 
- **NEVER** run an out-of-support release
- Ensure you have a plan to upgrade before the version's "end of life" date.

## Setting the Node.js major version

- To switch the default version of Node.js for all users, use the
`/QOpenSys/pkgs/bin/nodever` utility. For instance, for Node.js version 10 to be
the default, run `/QOpenSys/pkgs/bin/nodever 14`
- If you need to explicitly invoke a specific major version of Node.js, the
executable is found at `/QOpenSys/pkgs/lib/nodejs<version>/bin/node`, where
`<version>` is the major version. For instance, to run Node.js version 10, one
could run `/QOpenSys/pkgs/lib/nodejs10/bin/node`
- To switch the default version of Node.js for a specific user, place
`/QOpenSys/pkgs/lib/nodejs<version>/bin` at the beginning of the user's PATH
environment variable, similar to what's documented [here](SETTING_PATH.md).
For instance, that user could run the following from the shell to set their
default to version 16:

```bash
echo 'PATH=/QOpenSys/pkgs/lib/nodejs16/bin:/QOpenSys/pkgs/bin:$PATH' >> $HOME/.profile
echo 'export PATH' >> $HOME/.profile
```

(if using `bash` as the shell, the user may need to run `hash -r`)

## Globally-installed modules

- To use `node-gyp` (or other globally-installed modules) from the command line,
follow the same instructions in the previous section to add the version-specific
directory to your `PATH`
## Modules for accessing Db2, RPG, CL etc

- Be sure to use the `itoolkit` package from npm (`npm install itoolkit`) for accessing RPG, CL, etc.
- For database access, install one of the following packages from npm:
`idb-connector`, `idb-pconnector`, `odbc` (see [the ODBC doc](../odbc/README.md) for further guidance on ODBC)

## Coming from 5733-OPS?
- Any globally-installed modules must be reinstalled. Note, however, that global
installations of node modules are generally considered bad practice (with a few
exceptions, like `node-gyp`).


## Using Node Version Manager (nvm)

### Step 1: Install developer tools

From an SSH terminal, run:

```bash
yum group install "Development Tools"
yum install gcc10\*
```

### Step 2: Install NVM

First, install necessary prerequisites using [yum](../yum/) to verify that you
have curl and/or wget installed. Make sure you
[set your PATH](../troubleshooting/SETTING_PATH.md) to utilize the new open
source technology.

Then, simply follow the installation steps on the
[nvm project page](https://github.com/creationix/nvm/)

### Step 3: Configure your $HOME/.nvmrc file

Create a file at `$HOME/.nvmrc`, with the following contents

```bash
--dest-cpu=ppc64
--without-snapshot
--shared-openssl
--without-perfctr
```

### Step 4: Set necessary environment variables

Set the following environment variables:

```bash
OBJECT_MODE=64
CC=gcc-10
CXX=g++-10

```

Preferrably, set these in your `$HOME/.profile` and/or `$HOME/.bash_profile`
(depending on your shell settings), by adding the following lines:

```bash
OBJECT_MODE=64
export OBJECT_MODE
CC=gcc
export CC
CXX=g++
export CXX
```

### Step 5: Run nvm

NVM, like many open source commands, are best run from an SSH terminal. See the
[nvm project page](https://github.com/creationix/nvm/) for example usages of the
command. Some examples include:

* `nvm install stable` : install the latest stable version
* `nvm install --lts` : install the latest LTS release
* `nvm use --lts` : use the latest LTS release
