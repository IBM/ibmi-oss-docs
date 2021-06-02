# Release-specific IBM repositories

Some software is not available for all supported IBM i releases. As a result, some software is
distributed in release-specific repositories. in order to have access to these packages,
you may need to manually add the release-specific repository. 

## Installation

First, you need to install the `yum-utils` package:
```
yum install yum-utils
```

Then, you can use `yum-config-manager` to add the release-specific repository. Currently, only one
of these repositories has any packages, and that is the IBM i 7.3 repo. Note that the IBM i 7.3
repo can also be used for newer releases of IBM i. 

```
yum-config-manager --add-repo https://public.dhe.ibm.com/software/ibmi/products/pase/rpms/repo-7.3/
```
You do not need to disable any existing repositories.
