# Installing Python Packages

```{toctree}
:maxdepth: 1
```

See [Python usage notes](./README.md) for basic information.

## General Guidance (always try RPM first!)
For packages not listed in the above table, first check if it's available via
yum. If so, it is recommended to install it through yum instead of installing
it using pip.


### Installing native code with pip

If you must install using pip, make sure to invoke pip correctly (see
[Python usage notes](./README.md))

Also, you may need to install develompent tools, like gcc and automake, which you
can often do a la carte (`yum install gcc automake`) or you may need to install
the "Developer Tools" group (`yum install "Developer Tools"`). 

You will also need to set the following environment variables for build:
- `OBJECT_MODE=64`

If you have issues that you cannot debug, feel free to join the community channels
documented [here](http://ibm.biz/ibmioss)!

### gevent

When installing gevent, you may encounter a compile error such as:

```c
        c/_cffi_backend.c:15:17: fatal error: ffi.h: No such file or directory
         #include <ffi.h>
                         ^
        compilation terminated.
        error: command '/QOpenSys/pkgs/bin/gcc' failed with exit code 1
        [end of output]

    note: This error originates from a subprocess, and is likely not a problem with pip.
  error: legacy-install-failure

  × Encountered error while trying to install package.
  ╰─> cffi
```

This occurs because gevent uses cffi as a build requirement. Build requirements are built in an isolated enironment
We package cffi as an RPM. To use the cffi package as rpm do the following:

```bash
# install python39-cffi
yum install python39-cffi
# disable build isolation to use system cffi
pip3.9 install --no-build-isolation gevent
```
