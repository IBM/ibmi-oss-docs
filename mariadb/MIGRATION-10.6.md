ejbdccuuiigunbnjkbcidkhnfghknvvhbrredfjnektc
# Migrating from MariaDB 10.3.x MariaDB 10.6.x

```{toctree}
:maxdepth: 1
```

## Notable Differences

### [Binary Name Changes](https://mariadb.com/kb/en/upgrading-from-mariadb-104-to-mariadb-105/#binary-name-changes)
All binaries previously beginning with mysql now begin with mariadb, with symlinks for the corresponding mysql command.

Usually that shouldn't cause any changed behavior, but when starting the MariaDB server via the mysqld_safe script symlink, the server process will now always be started as mariadbd, not mysqld.

So anything looking for the mysqld name in the system process list, like e.g. monitoring solutions, now needs to check for mariadbd instead when the server / service is not started directly, but via mysqld_safe or as a system service.

### [Unix Socket Authentication](https://mariadb.com/kb/en/upgrading-from-mariadb-103-to-mariadb-104/#authentication-and-tls)

Since 10.4 MariaDB, switched to use the [unix_socket authentication plugin](https://mariadb.com/kb/en/authentication-plugin-unix-socket/) is now default on Unix-like systems. On IBM i this is disabled due to limitations in PASE.

### [Reserved Word](https://mariadb.com/kb/en/upgrading-from-mariadb-10-5-to-mariadb-10-6/#reserved-word)
New reserved word: OFFSET. This can no longer be used as an identifier without being quoted.

### [InnoDB COMPRESSED Row Format](https://mariadb.com/kb/en/upgrading-from-mariadb-10-5-to-mariadb-10-6/#innodb-compressed-row-format)
From MariaDB 10.6.0 until MariaDB 10.6.5, tables that are of the COMPRESSED row format are read-only by default. This was intended to be the first step towards removing write support and deprecating the feature.

This plan has been scrapped, and from MariaDB 10.6.6, COMPRESSED tables are no longer read-only by default.

From MariaDB 10.6.0 to MariaDB 10.6.5, set the innodb_read_only_compressed variable to OFF to make the tables writable.

### [Character Sets](https://mariadb.com/kb/en/upgrading-from-mariadb-10-5-to-mariadb-10-6/#character-sets)
From MariaDB 10.6, the utf8 character set (and related collations) is by default an alias for utf8mb3 rather than the other way around. It can be set to imply utf8mb4 by changing the value of the old_mode system variable.

**NOTE**:
For IBM builds the default character set and collations are set to utf8mb4 by default.

### [Disks Plugin](https://mariadb.com/kb/en/disks-plugin/)
The disk plugin as is now enabled by default and seems to function well.

### For full list of changes take a look at MariaDB upgrading docs:
- https://mariadb.com/kb/en/upgrading-from-mariadb-103-to-mariadb-104/#incompatible-changes-between-103-and-104
- https://mariadb.com/kb/en/upgrading-from-mariadb-104-to-mariadb-105/#incompatible-changes-between-104-and-105
- https://mariadb.com/kb/en/upgrading-from-mariadb-10-5-to-mariadb-10-6/#incompatible-changes-between-105-and-106

Also checkout the [MariaDB 10.6 release notes](https://mariadb.com/kb/en/changes-improvements-in-mariadb-106/) for more info.


## Migration Steps

MariaDB 10.6 conflicts with and is not co-installable with MariaDB 10.3.

1. Backup your existing data using [mysqldump](https://mariadb.com/kb/en/backup-and-restore-overview/#mysqldump)
	```sh
	# you will be prompted to enter the password
	mysqldump --all-databases --routines --events --user root --password
	```

2. Stop the MariaDB Server
	```sh
	# you will be prompted to enter the password
	mysqladmin shutdown --user root --password
	```

3. Remove MariaDB 10.3.x packages

	```sh
	yum remove mariadb-server mariadb
	```

4. Install MariaDB 10.6.x packages
	```sh
	yum install mariadb-10.6-server mariadb-10.6
	```

5. Start MariaDB 10.6.x Server


	```sh
	mariadbd-safe &
 	# NOTE: If the IPv6 interface is disabled you will need to explicity set the bind address
 	# For example:
 	# mariadbd-safe --bind-address=0.0.0.0 &
 	# Refer to the MariaDB docs for more info
 	# https://mariadb.com/kb/en/configuring-mariadb-for-remote-client-access/
 	# https://mariadb.com/kb/en/server-system-variables/#bind_address
	```
	
6. Run `mariadb-upgrade`  

	```sh
   # you will be prompted to enter the password
	mariadb-upgrade --user root --password
	```
