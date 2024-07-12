# IBM i Access ODBC Installation

```{toctree}
:maxdepth: 1
```

The instructions for installing and ODBC driver and manager and the IBM i ODBC
driver for Db2 on i will depend on what operating system you are running. Select
your operating system below to see setup instructions for getting ODBC on your
system and connected to IBM i.

* [IBM i](#ibm-i)
* [Linux](#linux)
* [Windows](#windows)
* [macOS](#macOS)

## IBM i

The ODBC driver for IBM i is provided in the `ibm-iaccess` package, so it can be
easily installed with `yum`. For instance:
```bash
yum install ibm-iaccess
```

Installing this RPM will do the following:
- Install the IBM i Access ODBC driver
- Install the `unixODBC` driver manager
- Register the driver with the driver manager by putting the appropriate information
in the `odbcinst.ini` file (see [using](./using.md)).
- Create a datasource name (DSN) for your local system called `*LOCAL`. This is
discussed further in the "[using](./using.md)" doc.

## Linux

IBM now has RPM and DEB repositories for Linux available directly from IBM for the
IBM i Access Client Solutions application package, which includes the IBM i
Access ODBC driver. 

On Linux, we will be using unixODBC as our driver manager. Fortunately, unixODBC
is automatically pulled in when you install the IBM i Access ODBC Driver for
Linux, so there isn't any set up that you have to do for this stage. If you want
to develop applications using ODBC packages like pyODBC for Python or odbc for
Node.js, you will have to manually use yum to install `unixODBC-devel` as well.

### Installing the Repository

The repositories are located under
<https://public.dhe.ibm.com/software/ibmi/products/odbc/>.

#### Red Hat-based Distribution Setup

```shell
curl https://public.dhe.ibm.com/software/ibmi/products/odbc/rpms/ibmi-acs.repo | sudo tee /etc/yum.repos.d/ibmi-acs.repo
```

#### SUSE-based Distribution Setup

```shell
curl https://public.dhe.ibm.com/software/ibmi/products/odbc/rpms/ibmi-acs.repo | sudo tee /etc/zypp/repos.d/ibmi-acs.repo
```

#### Debian-based and Ubuntu-based Distribution Setup

```shell
curl https://public.dhe.ibm.com/software/ibmi/products/odbc/debs/dists/1.1.0/ibmi-acs-1.1.0.list | sudo tee /etc/apt/sources.list.d/ibmi-acs-1.1.0.list
```

### Installing the ODBC driver

#### Red Hat-based Distribution Installation

```shell
sudo dnf install --refresh ibm-iaccess
```

#### SUSE-based Distribution Installation

```shell
sudo zypper refresh
sudo zypper install ibm-iaccess
```

#### Debian-based and Ubuntu-based Distribution Installation

```shell
sudo apt update
sudo apt install ibm-iaccess
```
## Windows

### Driver Manager for Windows

Windows comes preinstalled with an ODBC driver manager. To access it, search for
`Administrative Tools` on your system (either through the search bar, or
`Control Panel > System and Security > AdministrativeTools`), and then from
there select ODBC Data Sources (either 32-bit or 64-bit).

From this application, you can set up your drivers.

### Driver for Windows

You will have to install the ODBC driver that allows Windows ODBC driver manager
to talk to Db2 on i. To get the driver, visit
[the IBM i Access Client Solutions page](https://www-01.ibm.com/support/docview.wss?uid=isg3T1026805)
and select **Downloads for IBM i Access Client Solutions**. After logging in and
redirected to the IBM I Access Client Solutions download page, scroll down and
download the **ACS Windows App Pkg English (64bit)**.

When the package has been downloaded and has been installed on your system, it
should be available to see on your ODBC Data Source Administrator application.

## macOS

### Driver Manager for macOS

On macOS, you will need unixODBC as your ODBC driver manager. Many macOS ODBC
programs use another driver manager called **iodbc**, but *the IBM i ODBC driver
will not work with iodbc*. unixODBC is available from
[Homebrew](https://brew.sh), and can be installed running the following
command:

```shell
brew install unixodbc
```

### Driver for macOS

IBM now has a repository for the macOS driver as well. This repository is set
up as a [Tap](https://docs.brew.sh/Tap).


### Installing the Repository

The repositories are located under
<https://public.dhe.ibm.com/software/ibmi/products/odbc/macos>.


```shell
brew tap ibm/iaccess https://public.dhe.ibm.com/software/ibmi/products/odbc/macos/tap/
```

### Installing the ODBC driver

```shell
brew install ibm-iaccess
```
