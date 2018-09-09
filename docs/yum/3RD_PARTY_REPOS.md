# Third-party (non-IBM) repositories

The repositories listed on this page are not owned, managed, or supported by IBM. However, the repositories have been inspected and the software generally seems to be built with IBM-approved conventions for existing well in the IBM-delivered open source ecosystem. 

# Installation instructions
For each repository, this page lists a repo file and the contents for this repo file. In order to install this new repository, simply create the given repo file and populate it with the given contents using your favorite file editor. 


# Repository List

### The i Doctor
*Software offered:* lynx

*repo file:* `/QOpenSys/etc/yum/repos.d/the-i-doctor.repo`
 
*repo file contents:*

```
[the-i-doctor]
name=the-i-doctor
baseurl=http://the-i-doctor.com/oss/repo/ppc64
enabled=1
gpgcheck=0
```