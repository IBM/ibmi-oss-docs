# Deploying ASF TomCat on IBM i (using GitBucket as a sample application)

This simple guide is intended to help you deploy your first application in TomCat standalone mode. For
this exercise, we use [GitBucket](https://github.com/gitbucket/gitbucket) as a sample application.
You can similarly deploy any .war file using these steps


# Prerequisite setup
As with any open source software, it is recommended that you use an SSH
terminal session to perform these tasks. QSH or other 5250 interfaces may
work, but can be problematic.

## Run bash and set appropriate environment variables
These steps assume you are running with SSH and
[using bash as your default shell](../../troubleshooting/SETTING_BASH.md). 

If you're not running `bash`, you can run it explicitly:
```bash
exec /QOpenSys/pkgs/bin/bash
```

If you haven't already [customized your PATH to include open source](../../troubleshooting/SETTING_BASH.md),
you can do that temporarily:
```bash
export PATH=/QOpenSys/pkgs/bin:$PATH
```
## Choose installation and download directories
Save your installation and download directory in environment variables
(these are only used for convenience during the steps in this guide):
```bash
export DOWNLOAD=/opt/download
export TOMCAT=/opt/tomcat
```
The aboves assumes the following directories:
- TomCat installation directory: `/opt/tomcat`
- Download directory (when downloading TomCat and GitBucket): `/opt/download`

You may choose to download files or deploy WildFly anywhere on the filesystem.
Just change these values accordingly.

(subsequent steps assume you are using this same SSH session)


## Create installation directory and download directory
```bash
mkdir -p $DOWNLOAD
mkdir -p $TOMCAT
```

# Step 1: Install Required Software
```bash
yum install wget tar-gnu gzip nano openjdk-11
```

Alternatively, use Access Client Solutions to install these packages.

# Step 2: Download TomCat

## Technique 1: Using `wget`
(change the version number, if needed, to the version you would like to install)
```bash
cd $DOWNLOAD
https://dlcdn.apache.org/tomcat/tomcat-10/v10.0.14/bin/apache-tomcat-10.0.14.tar.gz
```

## Technique 2: Manual download
Just navigate to [the TomCat website](https://tomcat.apache.org/) and access the downloads from the navication pane
Download the latest version in .tar.gz format. Once downloaded, place in the download directory chosen earlier.

![image](https://user-images.githubusercontent.com/17914061/147589739-6954c981-784b-4965-a005-9c151b69d80c.png)



# Step 3: Install TomCat

(change the version number in the filename, if needed, to the proper version)
```bash
cd $DOWNLOAD
tar --strip-components=1 -C $TOMCAT -xzvf apache-tomcat-10.0.14.tar.gz
```

# Step 4: Configure TomCat to use Java of choice
Create a `setenv.sh` file located in the `/bin` directory of the WildFly installation directory.
This script will be called to set any needed environment variables, and can be used to set `JAVA_HOME`
to the location of our choosing. 
For this, you can use the editor of your choice (assuming you have a drive mapped with sshfs or NetServer),
or you can use a terminal-based editor like nano:
```bash
cd $WILDFLY/bin
touch setenv.sh
nano setenv.sh
```
Simply add the following lines (depending which Java you choose) and save the file

For OpenJDK:
```bash
JAVA_HOME="/QOpenSys/pkgs/lib/jvm/openjdk-11"
export JAVA_HOME
```
For JV1:
```bash
JAVA_HOME="/QOpenSys/QIBM/ProdData/JavaVM/jdk11/64bit"
export JAVA_HOME
```

