# Third-party (non-IBM) repositories

The repositories listed on this page are not owned, managed, or supported by
IBM. However, the repositories have been inspected and the software
generally seems to be built with IBM-approved conventions for existing well in
the IBM-delivered open source ecosystem.

## Installation instructions

First the `yum-utils` package should be installed. This provides the
`yum-config-manager` utility, which mades it easy to add new repositories, as
well as enable or disable existing repositories.

## Repository List

### PHP

**Brought to you by:** Perforce and IBM

**Software offered:** PHP and several PHP plugins

**Install**: `yum-config-manager --add-repo  http://repos.zend.com/ibmiphp/`

### OpenMax

**Brought to you by:** [Massimo Fantin](https://twitter.com/massimofantin)

**Software offered:** A large collection of open source packages, including Postgresql,
Ghostscript, Postfix , rddtool etc etc

**Install**: `yum-config-manager --add-repo ftp://openmax.duckdns.org/IBMi_Repo/openmax.repo`

## The i Doctor

**Brought to you by:** Jack Woehr

**Software offered:** lynx-dev (limited capabilities, for instance no https support).
schily-tools (cdrecord, mkisofs, etc.)

**Install**: `yum-config-manager --add-repo http://www.the-i-doctor.com/oss/repo/the-i-doctor.repo`

## QSECOFR

**Brought to you by:** Yvan Janssens

**Software offered:** Mono on i and various Open Source software for which fixes
have been accepted upstream to enable them to run on i.

**Install**: `yum-config-manager --add-repo http://repo.qseco.fr/qsecofr.repo`

## SoBored

**Brought to you by:** Josh Hall

**Software offered:** [ibmi-dotfiles](https://github.com/jbh/ibmi-dotfiles)

**Install**: `yum-config-manager --add-repo http://rpms.sobo.red/ibmi/`
