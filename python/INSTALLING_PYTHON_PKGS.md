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
