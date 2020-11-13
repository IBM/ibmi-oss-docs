# Using ODBC

Now that you have the IBM i Access ODBC Driver installed on your system, you are ready to connect to Db2 on i.

## Connection Strings

ODBC uses a connection string with keywords to create a database connection. Keywords are case insensitive, and values passed are separated from the keyword by an equals sign ("`=`") and end with a semi-colon ("`;`"). As long as you are using an ODBC database connector, you should be able to pass an identical connection string in language or technology and be confident that it will correctly connect to Db2 on i. A common connection string may look something like:

```
DRIVER=IBM i Access ODBC Driver;SYSTEM=my.ibmi.system;UID=foo;PWD=bar;
```

In the above example, we define the following connection options:
* DRIVER: The ODBC driver for Db2 for i that we are using to connect to the database (and that we installed above)
* SYSTEM: The location of your IBM i system, which can be its network name, IP address, or similar
* UID: The User ID that you want to use on the IBM i system that you are connecting to
* PWD: The password of the User ID passed above.

These are only some of the over 70 connection options you can use when connecting to Db2 on i using the IBM i Access ODBC Driver. A complete list of IBM i Access ODBC Driver connection options can be found at the [IBM Knowledge Center: Connection string keywords webpage](https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_74/rzaik/connectkeywords.htm). If passing connections options through the connection string, be sure to use the keyword labeled with **Connection String**.

## DSNs

As you add more and more options to your connection string, your connection string can become quite cumbersome. Luckily, ODBC offers another way of defining connection options called a DSN (datasource name). Where you define your DSN will depend on whether you are using Windows ODBC driver manager or unixODBC on Linux or IBM i.

### Configuration with UnixODBC (IBM i, Linux, macOS)

IBM i, Linux distributions, and macOS use unixODBC and have nearly identical methods of setting up your drivers and your DSNs.

**`odbc.ini` and `.odbc.ini`**

When using unixODBC, DSNs are defined in `odbc.ini` and `.odbc.ini` (note the `.` preceding the latter). These two files have the same structure, but have one important difference:

* `odbc.ini` defines DSNs that are available to **all users on the system**. If there are DSNs that should be available to everyone, they can be defined and shared here. Likely, this file is located in the default location, which depends on whether you are on IBM i or Linux:

* IBM i: `/QOpenSys/etc/odbc.ini`
* Linux: `/etc/unixODBC/odbc.ini`

If you want to make sure, the file can be found by running:

```
$ odbcinst -j
```

* `.odbc.ini` is found in your home directory (`~/`) and defines DSNs that are available **only to you**. If you are going to define DSNs with your personal username and password, this is the place to do it.

In both `odbc.ini` and `.odbc.ini`, you name your DSN with `[]` brackets, then specify keywords and values below it. An example of a DSN stored in `~/.odbc.ini` used to connect to an IBM i system with private credentials might look like:

```ini
[MYDSN]
Description            = My IBM i System
Driver                 = IBM i Access ODBC Driver
System                 = my.ibmi.system
UserID                 = foo
Password               = bar
Naming                 = 0
DefaultLibraries       = MYLIB
TrueAutoCommit         = 1
```

(**Note:** The name of the driver specified in the `Driver` keyword must match the name of a driver defined in `odbcinst.ini`. The location of this file can also be found by running `odbcinst -j` in PASE. When you install the IBM i Access ODBC Driver on your system, it automatically creates a driver entry of `IBM i Access ODBC Driver` in `odbcinst.ini`, which you should use for all IBM i connections).

When installing the IBM i Access ODBC Driver on IBM i, the driver will automatically create a DSN called `[*LOCAL]` in your `odbc.ini`:

```ini
### IBM provided DSN - do not remove this line ###
[*LOCAL]
Description = Default IBM i local database
Driver      = IBM i Access ODBC Driver
System      = localhost
UserID      = *CURRENT
### Start of DSN customization
### End of DSN customization
### IBM provided DSN - do not remove this line ###
```

When using this DSN, the user credentials used will be `*CURRENT`, which is the user who is running the process that is trying to connect to the ODBC driver. Use of this `*CURRENT` behavior is dependent on some server PTFs:

* 7.2: SI68113
* 7.3: SI69058
* 7.4: (none, comes with the operating system)

Like connection string keywords, DSN keywords can be found at the [IBM Knowledge Center: Connection string keywords webpage](https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_74/rzaik/connectkeywords.htm). When passing connection options through a DSN, be sure to use the keyword labeled with **ODBC.INI**.

### Configuration on Windows

When you have the driver installed on your system, you can now configure your datasource names (DSNs) that allow you to wrap all of your connection settings in one place that can be used by any ODBC application.

In ODBC Data Source Administrator, you can define either User DSNs or System DSNs. A User DSN will be available only to your Windows user, while a System DSN will be available to everyone. Furthermore, System DSNs must be defined per-architecture, while User DSNs are architecture agnostic.

To create a DSN, select either User DSN or System DSN and then select `Add` on the right-hand menu. It will prompt you to select a driver, and you will select `IBM i Access ODBC Driver`. Use the GUI to add configuration options, such as your username and passwords, threading, default library, and so on.

### Using Your DSN

Once you have DSNs defined with the connection options you want, you can simply pass a connection string to your ODBC connections that references the DSN:

```
DSN=MYDSN
```

This will look through your DSNs for a match, and pull in all connection options defined therein. This helps keep your connection string much more manageable, and also keeps your connections string more secure since you don't have to explicitly pass your password in plain text.

Additional options can
