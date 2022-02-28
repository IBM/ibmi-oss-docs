# Java 11 Early Access RPM

```{toctree}
:maxdepth: 1
```

A Java RPM is now available, via the `openjdk-11-ea` packages! Note, however,
this is not considered generally available (GA). It is an early access package ONLY.

This page is here to address some frequently asked questions you may have.

## Is this Java production-ready?

No! These are early access RPMs, denoted with the `-ea` suffix in the package name.

## Why is this only "early access"?

Currently, this Java runtime has not yet completed all testing and is therefore
not certified as production ready. We have, however, done thorough functional
testing of various workloads, including Apache Camel, ActiveMQ, Tomcat, maven,
Jenkins, etc. We are releasing an "early access" version to solicit feedback
from the IBM i community, and we welcome your feedback for any testing you do!

## How do I install this?

Simply use `yum` or the Open Source Package Management tool in
Access Client Solutions to install the `openjdk-11-ea` package.

## Where does this install?

The Java Runtime Environment (JRE) gets installed to `/QOpenSys/pkgs/lib/jvm/openjdk-11`

## How do I select this JVM to run my program?

If invoking Java directly from the command line, you will need to fully-qualify
the `java` binary (`/QOpenSys/pkgs/lib/jvm/openjdk-11/bin/java`) or add the
executable's directory to the beginning of your PATH, like so:

```bash
PATH=/QOpenSys/pkgs/lib/jvm/openjdk-11/bin:$PATH
export PATH
```

If you'd like common Java-based tools, such as activemq or maven, to use this
Java, you should also set the `JAVA_HOME` environment variable:

```bash
JAVA_HOME=/QOpenSys/pkgs/lib/jvm/openjdk-11
export JAVA_HOME
```

## Why do I get error "Directory /QOpenSys/pkgs/lib/jvm/openjdk-11 in the JAVA_HOME environment variable does not contain a Java Virtual Machine."?

The default java launchers do not currently accommodate this open source distribution.
This will likely be investigated and addressed in a future release. In the
interim, launch Java explicitly as documented in the previous section.

## Can this integrate with RPG via the *JAVA declaration?

No.
This will likely be investigated for a future release.

## Can I use ILE native methods?

No, and there are no plans to support this. Instead, use the JTOpen (jt400)
library's `ProgramCall` support.
This also means that the `*CURRENT` special value cannot be used for
authentication with the JTOpen library.

## Does this show up in WRKJVMJOB?

No.
This will likely be added in a future release.

## Can this run inside of a chroot container?

Yes!! Unlike JV1 flavors of Java, this open source version is container-friendly.

## Are there any functions known not to work?

As previously stated, not all testing has been completed, and this is not
considered production-ready.
That being said, the `sun.nio.ch.AixAsynchronousChannelProvider` class will
malfunction and cause program crashes on IBM i 7.2. On IBM i 7.3, this function
requires PTF SI71837. For IBM i 7.4, PTF SI72224 is required.
