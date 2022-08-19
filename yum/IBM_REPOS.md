# IBM Repositories

```{toctree}
:maxdepth: 1
```

IBM provides a set of repositories to use with yum. Previously, there was one repo called
"ibm" pointing [here](https://public.dhe.ibm.com/software/ibmi/products/pase/rpms/repo).
Since the end of 2021, this repo has been deprecated and obsoleted by the repos provided
by the ibmi-repos package.

The ibmi-repos package is now required by yum and contains two repos:

- ibmi-release
- ibmi-base

The ibmi-release repo points to a release-specific directory. Depending on what IBM i
version you are running, the repo will dynamically determine the correct path use. This
repo will contain rpms which are applicable to that specific release.

The ibmi-base repo will contain packages which are applicable to all releases supported by
that repo (ie. there's a minimum release). Over time, this repo will change as older IBM i
releases go out of support and a new minimum release base repo is created.

Since August 18 2022, IBM i 7.3+ systems will see an ibmi-repos update in the ibmi-release
repo. This update changes the ibmi-base repo URL from the old [7.2+ repo](https://public.dhe.ibm.com/software/ibmi/products/pase/rpms/repo)
to the new [7.3+ repo](https://public.dhe.ibm.com/software/ibmi/products/pase/rpms/repo-base-7.3/).

IBM i 7.2 users are unaffected, since the 7.2 ibmi-release repo does not have the update.
Users still on IBM i 7.2 can continue using the old repo (and systems can still be bootstrapped
using the [7.2 bootstrap](https://public.dhe.ibm.com/software/ibmi/products/pase/rpms/bootstrap-7.2/)),
however there will be no more updates to 7.2 packages - security or otherwise. Users still on
IBM i 7.2 are encouraged to update to IBM i 7.3 or newer, supported release.

## Transition

Since December 2021, any system using a current bootstrap will start with the ibmi-repos
package installed. Any system set up using a prior bootstrap will not have the ibmi-repos
package and will instead have an ibm.repo file. See the FAQs below for how to deal with
the old repo file.

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

