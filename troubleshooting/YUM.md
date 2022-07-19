# Troubleshooting Yum problems

This page is designed to help you do problem determination for scenarios where yum itself is not working.
That is, you are having trouble getting RPM packages installed. 

## Before you go further.....

To make sure you're seeing the latest updates available for your operating system, make sure you have
the latest version of `yum` and `ibmi-repos` installed.
```
/QOpenSys/pkgs/bin/yum upgrade yum ibmi-repos
```

If you are able to successfully install the `ibmi-repos` package, you can consider removing the
legacy repo definition by running:

```
mv /QOpenSys/etc/yum/repos.d/ibm.repo /QOpenSys/etc/yum/repos.d/ibm.repo.backup
```


## RPM database corruption
If the RPM database is corrupt, you will receive errors about being unable to open the RPM database. 
The most common is: 

```
Error: Error: rpmdb open failed
```

**Solution:**

```
/QOpenSys/pkgs/bin/rpm --rebuilddb
```


## IFS Journaling

If you encounter an error like the following:

```text
error: db4 error(19) from dbenv->open: The specified device does not exist.
error: cannot open Packages index using db4 - The specified device does not exist. (19)
error: cannot open Packages database in /QOpenSys/var/lib/rpm
CRITICAL:yum.main:
Error: rpmdb open failed 
```

You probably have journalling on for an IFS directory that rpm is using. rpm
uses `mmap` to open its database files, which is incompatible with journaling.

*Note: When an ILE a application tries to `mmap` an IFS file which is being
journaled it gets an error - `ENOTSUP` (operation not supported), however this
gets mapped to PASE as `ENODEV` (no such device) which makes things confusing.*

**Solution:**

Ensure that journaling is disabled/omitted for `/QOpenSys/var/lib/rpm` or any
subdirectory. You can use option 8 from `WRKLNK` to view the journaling
attributes of a given file or directory.

## yum can't connect to the repository from QSH

When running yum from QSH, any commands that connect to the repository (install
upgrade, etc) fail with a message like so:

```sh
yum install python3
https://public.dhe.ibm.com/software/ibmi/products/pase/rpms/repo/repodata/repomd.xml: [Errno 14] curl#6 - "getaddrinfo() thread failed to start"
Trying other mirror.
Error: Cannot retrieve repository metadata (repomd.xml) for repository: ibm. Please verify its path and try again
```

**Solution:**

Run yum via SSH or the ACS Open Source Package Manager GUI. These are the ideal
interfaces for working with yum and the rest of the open source ecosystem.

If you need to work from 5250, QP2TERM is preferred over QSH, but QSH _will_
work as long as the `QIBM_MULTI_THREADED` environment variable is set to `Y` at
the job level.


## Checking Connectivity

The most common cause of issue with yum is related to network connectivity. Errors will state something like
```
unable to open repomd.xml
```

The IBM server supports three protocols for downloading packages:
- HTTPs (secure, default, recommended)
- HTTP (disabled by default)
- FTP (disabled by default)

HTTP or FTP can be used as a backup mechanism if you are unable to get the default configuration working, or if your network
prohibits https connections. 

You can use Python to check connectivity to the IBM RPM server. To check if you have HTTPS connectivity and have proper
TLS setup, run:

```python
/QOpenSys/pkgs/bin/python2.7 -c "import socket; import ssl; hostname='public.dhe.ibm.com'; ssl.create_default_context().wrap_socket(socket.create_connection((hostname,443), 30), server_hostname=hostname) ; print 'success'"
```

The output from this command can help you figure out next steps:
- If the output contains `Hostname and service name not provided or found`, DNS is not configured properly
- If the output contains `timed out` or `connection refused` then you cannot reach IBM's server
- If the output contains `ssl.CertificateError: hostname '______________' doesn't match 'public.dhe.ibm.com'`, a separate entity is injecting an SSL certificate
- If the output contains another CertificateError, you need to install the `ca-certificates-mozilla` package

## Checking Connectivity for alternative protocols

**To check if you have HTTPs connectivity:**

```python
/QOpenSys/pkgs/bin/python2.7 -c "import socket; socket.create_connection(('public.dhe.ibm.com', 80), 30); print 'success'"
```

**To check for HTTP connectivity**

```python
/QOpenSys/pkgs/bin/python2.7 -c "import socket; socket.create_connection(('public.dhe.ibm.com', 80), 30); print 'success'"
```

**To check for FTP connectivity:**

```python
/QOpenSys/pkgs/bin/python2.7 -c "import socket; socket.create_connection(('public.dhe.ibm.com', 21), 30); print 'success'"
```

The output from this command can help you figure out next steps:
- If the output contains `Hostname and service name not provided or found`, DNS is not configured properly
- If the output contains `timed out` or `connection refused` then you cannot reach IBM's server


### DNS not configured properly

If DNS is not configured properly, please work with your IBM i system administrator or networking team to resolve the problem correctly. 

As a stopgap workaroud, you can create a host table entry for the IBM server at `public.dhe.ibm.com`.

**Important Note: This IP address may change in the future. At which point, yum will start failing and you will need to create new host table entries**

From SSH or QP2TERM:
```
system "ADDTCPHTE INTNETADR('129.35.224.112') HOSTNAME((public.dhe.ibm.com))"
```

From 5250 CL:
```
ADDTCPHTE INTNETADR('129.35.224.112') HOSTNAME((public.dhe.ibm.com))
```

### Cannot reach IBM's server

Please work with your networking team to resolve the problem.

### A separate entity is enjecting an SSL certificate

Follow [these steps](https://www.seidengroup.com/2021/04/26/how-to-validate-self-signed-ssl-tls-certificates-from-ibm-i/)
to add the new certificate as needed. 

## Installing `ca-certificates-mozilla` by enabling unsecure repos


## Installing ca-certificates-mozilla by disabling SSL verification

If you have the `ibmi-repos` package installed:

```
/QOpenSys/pkgs/bin/yum-config-manager --save --setopt=ibmi-base.sslverify=0
/QOpenSys/pkgs/bin/yum-config-manager --save --setopt=ibmi-release.sslverify=0
```
Otherwise: 

```
/QOpenSys/pkgs/bin/yum-config-manager --save --setopt=ibm.sslverify=0
```

Then, proceed to install the `ca-certificates-mozilla` package

Then, set the `sslverify` property back to `1`

If you have the `ibmi-repos` package installed:

```
/QOpenSys/pkgs/bin/yum-config-manager --save --setopt=ibmi-base.sslverify=1
/QOpenSys/pkgs/bin/yum-config-manager --save --setopt=ibmi-release.sslverify=1
```
Otherwise: 

```
/QOpenSys/pkgs/bin/yum-config-manager --save --setopt=ibm.sslverify=1
```
 

## Other Networking problems

### Operation too slow

```
'Operation too slow. Less than 1000 bytes/sec transferred the last 30 seconds'
```


## What if I cannot access the Internet from my IBM i system?

Doc forthcoming...
