# IBM Repositories

IBM provides a set of repositories to use with yum. Currently, this is one repo called "ibm" pointing [here](https://public.dhe.ibm.com/software/ibmi/products/pase/rpms/repo). This repo file is setup and enabled during the bootstrap
installation, however admins are free to disable or change this file at their discretion.

A change has been pushed out to yum and the bootstrap to install the "ibmi-repos" package which provides two new repos:
- ibmi-base
- ibmi-release

The ibmi-base repo will point to the same location as ibm (at least for now), making the ibm repo redundant and can be removed manually.

The ibmi-release is a new repo that points to a release-specific directory. Depending on what IBM i version you are running, the repo will dynamically determine the correct path to point to. This repo will contain rpms which are built specifically for each IBM i release.


## Transition

Currently, the ibm repo is provided by the bootstrap, but is not owned by a package. Because admins may have modified this file and it's not tracked by rpm, the decision was made to replace this file with a new repo file in the rpm. This means any modifications will not be overwritten by the new rpm, but it does mean that you may have a superfluous repo file that has to be cleaned up manually.


## FAQs

### Why are you making this change?

By providing the IBM repos in an rpm, it allows us to push out updates to our repo files using the same yum update mechanism.


Some examples of changes may include:

- The path to repo needs to change
- The protocol changes (FTP -> HTTPS)
- We start signing our repo metadata
- etc


### Why are you adding a new ibm-base repo instead of updating the existing repo?

Because ibm.repo is not tracked by rpm, it becomes tricky to take over ownership of the file by rpm while preventing any local modifications from being overwritten while also being a seamless transition for users. By providing a new repo file, all users will immediately get access to the new repo because there are no conflicts with existing repo files. This also allowed us to give the repo a more meaningful name.

### What if I've deleted or disabled the ibm repo file?

Because the ibmi-repos package ships new repo files, the existing repo file is unaffected. However, the new repos _will_ be enabled by default. You can disable them using `yum-config-manager --disable ibmi-base ibmi-release`

Note that the new repo files are shipped with `skip_if_unavailable=1` set. This means that if you've disabled the ibm repo because your system does not have internet access, these repo files will not cause yum failures, but only warnings like

```text
https://public.dhe.ibm.com/software/ibmi/products/pase/rpms/repo-7.4/repodata/repomd.xml: [Errno 14] HTTPS Error 404 - Not Found
Trying other mirror.
```

### What if I've made changes to the existing ibm repo file?

Because the ibmi-repos package ships new repo files, the existing repo file is unaffected. It is recommended to rename the ibm.repo and disable the new repos with `yum-config-manager --disable ibmi-base ibmi-release` or manually apply your changes to the new repo files.

### What happens if I make changes to the new ibmi-base or ibmi-release repos?

Both of these files are marked as special config files inside rpm, which means that rpm will detect if they've been modified and if so it **will not** overwrite them. Instead, you will see a message from yum:

```text
warning: /QOpenSys/etc/yum/repos.d/ibmi-base.repo created as /QOpenSys/etc/yum/repos.d/ibmi-base.repo.rpmnew
```

It is up to you to look at the .rpmnew file to see what changes have been made and, if applicable, adjust the repo file accordingly.

### You said ibm and ibmi-base point to the same location; will that cause any problems?

There should not be any problems with both ibm and ibmi-base pointing to the same location. Yum will see two repos providing the same packages and will pick one when it goes to install updates.

Though there should be no problems having them both enabled, it's recommended that you disable the ibm repo using `yum-config-manager --disable ibm`. Once you have verified yum continues to work without it enabled, you can remove it using `rm /QOpenSys/etc/yum/repos.d/ibm.repo`.

### What should I do with the existing ibm repo file?

This repo is no longer needed as the ibmi-base repo supersedes it. It's recommended that you disable the ibm repo using `yum-config-manager --disable ibm`. Once you have verified yum continues to work without it enabled, you can remove it using `rm /QOpenSys/etc/yum/repos.d/ibm.repo`.

### Can I remove the ibmi-repos package?

No, yum has been made to depend on it and yum will prevent removing itself.

If you do not want these new repo files to be enabled, you can disable them using `yum-config-manager --disable ibmi-base ibmi-release`.

### Will the ACS clone tool work with the new repos?

Yes, the ACS clone tool should work with any repository.

### Will the ACS yum proxy work with the new repo?

Yes, the ACS yum proxy should work with all HTTP-based repositories.

