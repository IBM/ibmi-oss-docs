# Troubleshooting Yum problems

This page is designed to help you do problem determination for scenarios where yum itself is not working.
That is, you are having trouble getting RPM packages installed. 

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


## Debugging Network-related problems

You can use Python to check connectivity to the IBM RPM server. To check connectivity for the default
configuration, which uses HTTPS, run the following command from SSH or (if desparate) QP2TERM:

```python
/QOpenSys/pkgs/bin/python2.7 -c "import socket; import ssl; hostname='public.dhe.ibm.com'; ssl.create_default_context().wrap_socket(socket.create_connection((hostname,443), 30), server_hostname=hostname) ; print 'success'"
```

Alternatively, if you have customized your installation to use HTTP:

```python
/QOpenSys/pkgs/bin/python2.7 -c "import socket; socket.create_connection(('public.dhe.ibm.com', 80), 30); print 'success'"
```

Or ftp:

```python
/QOpenSys/pkgs/bin/python2.7 -c "import socket; socket.create_connection(('public.dhe.ibm.com', 21), 30); print 'success'"
```

The output from this command can help you figure out next steps:
- If the output contains `Hostname and service name not provided or found`, DNS is not configured properly
- If the output contains `timed out` or `connection refused` then you cannot reach IBM's server
- If the output contains `ssl.CertificateError: hostname '______________' doesn't match 'public.dhe.ibm.com'`, a separate entity is injecting an SSL certificate

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


