# OpenSSL 3.0 Migration

On August 12, 2024 IBM has shipped out updates to various packages using
OpenSSL. These updates switches the version of OpenSSL these packages use to
use OpenSSL 3.0 instead of OpenSSL 1.1.1 (which is no longer supported by the
OpenSSL project).

## Upgrade Risk

This change brings potential risk of application crash if OpenSSL 1.1.1 and
OpenSSL 3.0 are loaded in to the same process and the software is built with
runtime linking enabled (the default in the open source ecosystem). This can
happen even for software that does not use OpenSSL itself, but relies on other
packages which do use OpenSSL. For example, Python's `ssl` package directly
loads OpenSSL and the PyCurl package _indirectly_ loads OpenSSL through the
Curl library, which links to it. If the `ssl` package is linked to one version
of OpenSSL and the Curl library gets updated to use a different version of
OpenSSL, this could cause the software to crash.

## Mitigations

The good news is that changes have been put in place to mitigate these problems
as much as possible. Software provided by IBM has been modified to use
different compilation options to disable runtime linking for software using
OpenSSL (either directly or indirectly). By disabling runtime linking, this
allows OpenSSL 1.1.1 and OpenSSL 3.0 to coexist in the same process. In
addition, rules have been added to various packages such as Curl, Python, etc
that will prevent certain packages being upgraded unless packages requiring
mitigation have been updated.

It is still recommended to update all affected packages so that they use the
supported OpenSSL 3.0, but there should be no issues for mismatched
environments where only some of them are updated and some still use older
OpenSSL versions.

## Diagnosis

Here's how to diagnose the issue if you happen to run in to this problem.
Again, all IBM software _should_ be mitigated however third-party software may
not be mitigated yet. The typical result will be the following generic error
message:

```text
Segmentation fault (core dumped)
```

A typical backtrace might look something like this:

```text
#0  0x090000000c2e9cfc in ?? () from /QOpenSys/pkgs/lib/libcrypto.so.1.1(shr_64.o)
#1  0x090000000c387018 in ?? () from /QOpenSys/pkgs/lib/libcrypto.so.1.1(shr_64.o)
#2  0x090000000c387018 in ?? () from /QOpenSys/pkgs/lib/libcrypto.so.1.1(shr_64.o)
#3  0x090000000c8e62d4 in ?? () from /QOpenSys/pkgs/lib/libcrypto.so.3(shr_64.o)
#4  0x090000000c8e65c4 in ?? () from /QOpenSys/pkgs/lib/libcrypto.so.3(shr_64.o)
#5  0x090000000c8bf718 in ?? () from /QOpenSys/pkgs/lib/libcrypto.so.3(shr_64.o)
#6  0x090000000c8bfcd8 in ?? () from /QOpenSys/pkgs/lib/libcrypto.so.3(shr_64.o)
#7  0x090000000c7ca654 in ?? () from /QOpenSys/pkgs/lib/libssl.so.3(shr_64.o)
#8  0x090000000c798c0c in ?? () from /QOpenSys/pkgs/lib/libssl.so.3(shr_64.o)
#9  0x090000000c798ff0 in ?? () from /QOpenSys/pkgs/lib/libssl.so.3(shr_64.o)
#10 0x090000000c6d490c in ?? () from /QOpenSys/pkgs/lib/libcurl.so.4(shr_64.o)
#11 0x090000000c6d5ab8 in ?? () from /QOpenSys/pkgs/lib/libcurl.so.4(shr_64.o)
#12 0x090000000c6cd9e8 in ?? () from /QOpenSys/pkgs/lib/libcurl.so.4(shr_64.o)
#13 0x090000000c6b8fec in ?? () from /QOpenSys/pkgs/lib/libcurl.so.4(shr_64.o)
#14 0x090000000c6c7a60 in ?? () from /QOpenSys/pkgs/lib/libcurl.so.4(shr_64.o)
#15 0x090000000c6b8fec in ?? () from /QOpenSys/pkgs/lib/libcurl.so.4(shr_64.o)
#16 0x090000000c73adec in ?? () from /QOpenSys/pkgs/lib/libcurl.so.4(shr_64.o)
#17 0x090000000c6b9ff4 in ?? () from /QOpenSys/pkgs/lib/libcurl.so.4(shr_64.o)
#18 0x090000000c6b0f9c in ?? () from /QOpenSys/pkgs/lib/libcurl.so.4(shr_64.o)
#19 0x090000000c6b27c8 in ?? () from /QOpenSys/pkgs/lib/libcurl.so.4(shr_64.o)
#20 0x090000000c6ab204 in ?? () from /QOpenSys/pkgs/lib/libcurl.so.4(shr_64.o)
```

Here, a function at frame 3 is in libcrypto.so.3 and then at frame 2, is in
libcrypto.so.1.1.So somehow an OpenSSL 3 function is inadvertently calling an
OpenSSL 1.1.1 function, causing a segmentation fault due to improperly
initialized memory or binary incompatibilities between version 3.0 and 1.1.1 of
OpenSSL. Luckily, this _specific_ problem shown from Python should no longer be
an issue.

## Third Party Software

There is still some risk for third party applications. Please consult with your
third party application vendors to ensure that their software is rebuilt with
OpenSSL 3.0 and/or is disabling runtime linking.

Seiden Group has a version of PHP available which disables runtime linking.
