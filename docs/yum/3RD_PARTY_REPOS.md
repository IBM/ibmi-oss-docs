# Third-party (non-IBM) repositories

The repositories listed on this page are not owned, managed, or supported by IBM. However, the repositories have been inspected and the software generally seems to be built with IBM-approved conventions for existing well in the IBM-delivered open source ecosystem. 

# Installation instructions
For each repository, this page lists a repo file and the contents for this repo file. In order to install this new repository, simply create the given repo file and populate it with the given contents using your favorite file editor. 


# Repository List

### The i Doctor
**Brought to you by:** Jack Woehr

**Software offered:** lynx-dev (limited capabilities, for instance no https support). schily-tools (cdrecord, mkisofs, etc.)

**repo file:** `/QOpenSys/etc/yum/repos.d/the-i-doctor.repo`
 
**repo file contents:**

```
[the-i-doctor]
name=the-i-doctor
baseurl=http://the-i-doctor.com/oss/repo/ppc64
enabled=1
gpgcheck=0
```

### QSECOFR
**Brought to you by:** Yvan Janssens

**Software offered:** Mono on i and various Open Source software for which fixes have been accepted upstream to enable them to run on i.

**repo file:** `/QOpenSys/etc/yum/repos.d/qsecofr.repo`
 
**repo file contents:**

```
[qsecofr]
name=QSECOFR IBM i RPM Repo
baseurl=http://repo.qseco.fr
enabled=1
gpgcheck=0
```

### SoBored
**Brought to you by:** Josh Hall

**Software offered:** [ibmi-dotfiles](https://github.com/jbh/ibmi-dotfiles)

**repo file:** `/QOpenSys/etc/yum/repos.d/sobored.repo`
 
**repo file contents:**

```
[sobored]
name=sobored
baseurl=http://rpms.sobo.red/ibmi/ppc64/
enabled=1
gpgcheck=0
```