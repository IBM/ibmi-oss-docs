# Why ODBC

```{toctree}
:maxdepth: 1
```

For the open-source software team, ODBC is the preferred method of connecting to
Db2 on i. There are many resons for this, including:

* Because ODBC is a technology that is used for more than just IBM i, there are
many applications and technologies that are already enabled to use ODBC. Nearly
all open-source programming languages (and many non-open-source languages) have
some way to connect to databases through an ODBC interface, facilitating
interaction with any database that has an ODBC driver (including IBM i).

* Similarly, because ODBC connectors have already been developed for so many
languages and frameworks, the IBM i Open-Source Software Team doesn’t have to
spend time creating specific Db2 for i connectors for every new technology we
deliver on the platform. This means that we can spend more time delivering new
software for you and pushing what is possible on IBM i. In the future, most of
the packages we develop will require that you use ODBC connections.

* As already mentioned, ODBC is useful if you want to connect to Db2 on i from
off-system. Unlike CLI-based connectors, which can only be built on IBM i, ODBC
connections can be created from Windows and Linux machines as well. This means
that you can develop your applications on one system and then move them to IBM i
when you are ready to deploy them. It also means that you can have the same
application running on multiple different platforms that can all communicate
with Db2 on i in the same way.

* Finally, there are many more connection options available for ODBC than on
CLI. When you create an ODBC connection through a DSN or a connection string,
there are approximately 70 different connection options that can be set. This
includes everything from specifying the system, your username, or your password,
to defining default libraries and schemas or whether or not stored procedures
can be called. A full list of options can be found on the
[“Connection string keywords” page of the 7.4 documentation](https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_74/rzaik/connectkeywords.htm).
