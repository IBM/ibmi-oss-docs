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


### reportlab

When installing reportlab, you may encounter a compile error such as:

```c
    src/rl_addons/renderPM/libart_lgpl/art_pixbuf.h:38:41: error: expected ';', ',' or ')' before '.' token
    typedef void (*ArtDestroyNotify) (void *func_data, void *data);
                                            ^
```

This is due to a conflict in the reportlab source code and the AIX header files. As a workaround, you can define `_LINUX_SOURCE_COMPAT` to prevent the conflicting definition:

```bash
 CFLAGS=-D_LINUX_SOURCE_COMPAT pip3.9 install reportlab
```
