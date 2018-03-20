# RPM pile (beta) for IBM i 7.2+
Much of the open source technology available in the 5733-OPS product is now available in RPM form. For instructions on getting started, please see [RPMs - Getting Started]()

**Beta status general note:** While the software has been tested and meets quality guidelines, the RPM form of this software, as well as the "yum" package manager, are in "beta" form. This beta targets IBM i 7.2 and newer.

 

## What's included in the beta?
Many things are currently available in RPM form. The RPMs - Getting Started page demonstrates how to use the "yum" package manager to see the entire list of what packages are available.

**Some notable deliveries include:**

- Node.js version 8
- Python 3.6
- The 'less' utility
- Git
- The 'updatedb' and 'locate' utilities (in the 'findutils' package)
- GCC 6.3.0 and many development tools such as automake, autoconf, m4, libtool, etc.
- GNU versions of many common utilities such as ls, grep, sed, awk.....
- GNU Nano
- many, many more things.....
 
## FAQ
**When will tools and language runtimes be 64-bit enabled?**

Most of the software available in RPM form is 64-bit, including the Python and Node.js runtimes


**Will 5733-OPS be updated to ship Node.js version 8, Python 3.6, or other goodies that are currently in RPM form only?**

There are currently no plans to deliver these packages in the 5733-OPS installable product. If you have a business need for such, please submit an RFE with your justification.


**Is this the same thing as Perzl.org or other RPM's I have heard of (or used) in the past?**

No. These RPM's are not AIX RPM's. They are IBM i RPMs shipping IBM i software. Built on IBM i, for IBM i.

**What if I am on IBM i 7.1?**

With the exception of a handful of packages (including Node.js), much of the software will still work, but IBM i 7.2+ is the target for this beta.