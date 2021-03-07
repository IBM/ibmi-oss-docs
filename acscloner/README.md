# ACS Clone Repo Tool

The "Clone Repo" tool is a tool that allows you to clone any http or
https-hosted RPM repository to the local Integrated File System (IFS) of the
target IBM i system.

## How do I launch the "Clone Repo" tool?

1. In Access Client Solutions, first access the Open Source Package Management
tool (Tools->"Open Source Package Management")
2. The clone tool is available after signing onto a system with the open source
package management tool (Utilities->"Clone Repo for Offline Use")

## Interface options, explained

### Source Repository

Specify the original repository that you'd like to take a clone/snapshot of.

### Destination (IFS)

Specify a target directory on IBM i for the clone/snapshot.

### Additional Operations -> Create or Update Repository Definition

The YUM package manager only knows about repos that are defined in YUM's
repository list. The repository list is simply a set of `.repo` files in the `/QOpenSys/etc/yum/repos.d/`

### Additional Operations -> Disable Repositories that Require Internet Access from the IBM i System

By default, YUM will fail any operations if it can't read from all the
configured repositories. This options disables Internet-requiring repos, so that
YUM operations continue to work. Keep this option checked if your IBM i system
can't access the Internet.

### Additional Operations -> Create nginx configuration file

Creates a configuration for the nginx http server to allow you to host this repo
clone via http, so that other systems in your network can access it (more
details below).

## Serving up your internal repo via nginx using ACS

The ACS "Clone Repo" tool makes it easy to serve your cloned repo to other
systems in your network. If you check the "create nginx configuration file"
option, the following files are created for you:

* nginx.conf: Used by nginx. By default, it configures nginx to use 5 worker
processes and listen on port 2055. Feel free to customize to suit your needs.
* startServer: Starts nginx as a background task in current subsystem.
* startServerBatch: Submits nginx to QHTTPSVR subsystem (feel free to customize
to suit your needs).
* stopServer: Stops the nginx instance

Of course, the next step is to configure other systems to point at your
newly-created repo. That can be done on endpoint systems either by:

1. installing `yum-utils` and invoking `yum-config-manager --add-repo <ip-address-where-hosted>`
(for instance, `yum-config-manager --add-repo http://mysystem:2055`).
2. creating a repository definition in `/QOpenSys/etc/yum/repos.d`. A repository
definition is a small text file with basic information. Use `ibm.repo` as an example.

To automate yum updates, one can use a job scheduler entry, specifying `-y` so
the YUM tool doesn't stop to ask for user confirmation. Example:
`ADDJOBSCDE JOB(YUMUP) CMD(QSH CMD('exec /QOpenSys/pkgs/bin/yum -y upgrade'))
FRQ(*WEEKLY) SCDDAY(*ALL)`
This example does a daily upgrade, but note that no update will happen if the
configured repo or repos have no changes. If the only configured repo is your
private one, then this will not do anything until you update your repo.

To summarize, the process of creating your own repository and hosting it for all
your systems involves:

1. Run the ACS Clone Repo Tool, checking the "Create nginx configuration file" box
2. Start the nginx server by running the `startServer`/`startServerBatch` script
3. Configure endpoint systems
4. (optional) automate

(A good practice might to to have a different repo for each class of systems,
such as development, test, and production)
