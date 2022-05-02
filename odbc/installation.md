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

### Driver Manager for Linux

On Linux, we will be using unixODBC as our driver manager. Fortunately, unixODBC
is automatically pulled in when you install the IBM i Access ODBC Driver for
Linux, so there isn't any set up that you have to do for this stage. If you want
to develop applications using ODBC packages like pyODBC for Python or odbc for
Node.js, you will have to manually use yum to install `unixODBC-devel` as well.

### Driver for Linux

To get both the unixODBC driver manager and the driver that allows ODBC to talk
to Db2 for i, you will have to install the IBM i Access ODBC Driver for Linux.
To get the driver, visit [the IBM i Access Client Solutions page](https://www-01.ibm.com/support/docview.wss?id=isg3T1026805)
and select **Downloads for IBM i Access Client Solutions**. After logging in and
redirected to the IBM I Access Client Solutions Download page, select the
`Download using http` tab then scroll down and download the **ACS Linux App Pkg**.

In this package, there is a README that will help explain how to install the
driver with either with RPMs or DEBs, depending on your Linux distribution. Just
know that when you install the driver, it should pull in all of the packages you
need to create an ODBC connection to Db2 for i from your Linux system.

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
will not work with iodbc*. unixODBC is available on `homebrew`, and can be
installed running the following command:

```shell
brew install unixodbc
```

### Driver for macOS

You will also have to install the macOS ODBC driver that allows unixODBC to talk
to Db2 on i. To get the driver, visit [the IBM i Access Client Solutions page](https://www-01.ibm.com/support/docview.wss?uid=isg3T1026805)
and select **Downloads for IBM i Access Client Solutions**. After logging in and
redirected to the IBM I Access Client Solutions download page, scroll down and
download the **ACS Mac App Pkg**. The package will include a standard macOS
installer package, which can be installed by double clicking orby running the
`pkgutil` command.
