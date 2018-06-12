First, install necessary prerequisites using [yum](https://bitbucket.org/ibmi/opensource/src/master/docs/yum/)

After doing so, you can set bash to be your default shell by running the following command from anywhere you have an SQL context, such as the Run SQL Scripts tool:

``` language=SQL
CALL QSYS2.SET_PASE_SHELL_INFO('*CURRENT', 
                               '/QOpenSys/pkgs/bin/bash');
```