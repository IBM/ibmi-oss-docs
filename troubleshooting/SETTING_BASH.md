# Setting BASH as your shell

```{toctree}
:maxdepth: 1
```

***The bash shell can (and should!) be your default shell for when you connect
with an SSH session. SSH connections are recommended for open source tools.
This will not affect the shell in use by non-SSH shell environments, such as
CALL QP2TERM or STRQSH***

First, install open source environment and [yum](../yum/README.md). Make sure
the `bash` package is installed (it should be, by default). After doing so, you
can set `bash` to be your default shell via one of the following techniques:

## Technique #1: chsh

1. Use yum to install the `chsh` package (for instamce, `yum install chsh`)

2. From a shell, use the `chsh` command to set your shell
  (for instance, `/QOpenSys/pkgs/bin/chsh -s /QOpenSys/pkgs/bin/bash`).
  You can set the shell for another user via the `-u` option
  (for instance, `/QOpenSys/pkgs/bin/chsh -s /QOpenSys/pkgs/bin/bash -u otherusr`).

## Technique #2: sql

You can set bash to be your default shell by running the following command from
anywhere you have an SQL context, such as the Run SQL Scripts tool:

```SQL
CALL QSYS2.SET_PASE_SHELL_INFO('*CURRENT', '/QOpenSys/pkgs/bin/bash')
```

You can also set bash to be the default shell for all users, by running:

```SQL
CALL QSYS2.SET_PASE_SHELL_INFO('*DEFAULT', '/QOpenSys/pkgs/bin/bash')
```

Or, for a specific user:

```SQL
CALL QSYS2.SET_PASE_SHELL_INFO('OTHRUSR', '/QOpenSys/pkgs/bin/bash')
```

More information on this IBM i service can be found on [developerWorks](https://www.ibm.com/developerworks/community/wikis/home?lang=en#!/wiki/IBM%20i%20Technology%20Updates/page/QSYS2.SET_PASE_SHELL_INFO%20Procedure)

Also, the default shell setting can be queried out with [QSYS2.USER_INFO](https://www.ibm.com/developerworks/community/wikis/home?lang=en#!/wiki/IBM%20i%20Technology%20Updates/page/QSYS2.USER_INFO%20catalog)
