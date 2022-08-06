# Troubleshooting Yum connection problems

This page is designed to help you do problem determination for scenarios where yum itself is not working
due to connection problems. That is, you are having trouble getting RPM packages installed. 

There are several `yum` problems that may not be connection related, and those are documented
on [the main troubleshooting page](README.md)

## Before you go further.....

To make sure you're seeing the latest updates available for your operating system, make sure you have
the latest version of `yum` and `ibmi-repos` installed, if you are able to. If you are unable to, read on. 
This page may still help
```
/QOpenSys/pkgs/bin/yum upgrade yum ibmi-repos
```

If you are able to successfully install the `ibmi-repos` package, you can consider removing the
legacy repo definition by running:

```
mv /QOpenSys/etc/yum/repos.d/ibm.repo /QOpenSys/etc/yum/repos.d/ibm.repo.backup
```


# Checking Connectivity

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

Then, set the `sslverify` property back to `1`. To do so, If you have the `ibmi-repos` package installed:

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

Sometimes, corporate network firewalls don't explicitly block ports, but they can drastically interfere with
traffic throughput, resulting in:

```
'Operation too slow. Less than 1000 bytes/sec transferred the last 30 seconds'
```

You can try working around this issue by enabling alternative protocols.

## Enabling alternative protocols

Assuming you have a modern version of `ibmi-repos` installed, you can try connecting with http or ftp if https does not work. To enable http and ftp mirrors:
```
/QOpenSys/pkgs/bin/yum-config-manager --enable-repo=ibmi-base-unsecure
/QOpenSys/pkgs/bin/yum-config-manager --enable-repo=ibmi-release-unsecure
```
(note this is unsecure and should be a temporary workaround until the http protocol issue is resolved by your networking team)

## Debug tool

You can download [this debug tool](https://raw.githubusercontent.com/ThePrez/IBMiOSS-utils/master/yum_conncheck.py), save it to IFS,
and run
```
/QOpenSys/pkgs/bin/python2.7 yum_conncheck.py
```
It will provide guidance

## TL;DR Steps that will fix most people that have a working DNS setup

```
/QOpenSys/pkgs/bin/yum-config-manager --save --setopt=ibm.sslverify=0
/QOpenSys/pkgs/bin/yum-config-manager --save --setopt=ibmi-base.sslverify=0
/QOpenSys/pkgs/bin/yum-config-manager --save --setopt=ibmi-release.sslverify=0
/QOpenSys/pkgs/bin/yum install ca-certificates-mozilla
/QOpenSys/pkgs/bin/yum upgrade ibmi-repos
/QOpenSys/pkgs/bin/yum-config-manager --disable-repo=ibm
/QOpenSys/pkgs/bin/yum-config-manager --save --setopt=ibmi-base.sslverify=1
/QOpenSys/pkgs/bin/yum-config-manager --save --setopt=ibmi-release.sslverify=1
```

## What if I cannot access the Internet from my IBM i system?

Doc forthcoming...
