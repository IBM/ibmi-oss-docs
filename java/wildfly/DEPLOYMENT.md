# Deploying WildFly on IBM i (using GitBucket as a sample application)

This simple guide is intended to help you deploy your first application in WildFly. For
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
(these are only used during the steps in this guide):
```bash
export DOWNLOAD=/opt/download
export WILDFLY=/opt/wildfly
```
The aboves assumes the following directories:
- WildFly installation directory: `/opt/wildfly`
- Download directory (when downloading WildFly and GitBucket): `/opt/download`

You may choose to download files or deploy WildFly anywhere on the filesystem.
Just change these values accordingly.

(subsequent steps assume you are using this same SSH session)


## Create installation directory and download directory
```bash
mkdir -p $DOWNLOAD
mkdir -p $WILDFLY
```

# Step 1: Install Required Software
```bash
yum install wget tar-gnu gzip nano openjdk-11
```

Alternatively, use Access Client Solutions to install these packages.

# Step 2: Download WildFly

## Technique 1: Using `wget`
(change the version number, if needed, to the version you would like to install)
```shell
cd $DOWNLOAD
wget https://github.com/wildfly/wildfly/releases/download/26.0.0.Final/wildfly-26.0.0.Final.tar.gz
```

## Technique 2: Manual download
Just navigate to [the WildFly website](https://www.wildfly.org/downloads/) and access the downloads.
Download the latest version in .tar.gz format. Once downloaded, place in the download directory chosen earlier.
![image](https://user-images.githubusercontent.com/17914061/146617098-cbd084eb-4529-47ee-b226-cf9bf3f837d3.png)


# Step 3: Install WildFly

(change the version number in the filename, if needed, to the proper version)
```bash
cd $DOWNLOAD
tar --strip-components=1 -C $WILDFLY -xzvf wildfly-26.0.0.Final.tar.gz
```

# Step 4: Configure WildFly to use Java of choice
Open the `standalone.conf` file located in the `/bin` directory of the WildFly installation directory.
For this, you can use the editor of your choice (assuming you have a drive mapped with sshfs or NetServer),
or you can use a terminal-based editor like nano:
```bash
cd $WILDFLY/bin
nano standalone.conf
```
The default `standalone.conf` file has a commented-out line with a `JAVA_HOME` value. Uncomment the line and
insert the appropriate JAVA_HOME value. You can choose between OpenJDK or JV1 versions of Java.

For OpenJDK:
```bash
JAVA_HOME="/QOpenSys/pkgs/lib/jvm/openjdk-11"
```
For JV1:
```bash
JAVA_HOME="/QOpenSys/QIBM/ProdData/JavaVM/jdk11/64bit"
```

# Step 5 : Configure server address (optional)
Open the `standalone.xml` file in the `standalone/configuration` directory
Open the `standalone.conf` file located in the `/bin` directory of the WildFly installation directory.
For this, you can use the editor of your choice (assuming you have a drive mapped with sshfs or NetServer),
or you can use a terminal-based editor like nano:
```bash
cd $WILDFLY/standalone/configuration/
nano standalone.xml
```

Search for the `<interfaces>` tag (in nano, this can be done with ctrl+W). You will find a section that defines
the management and public interfaces
```xml
    <interfaces>
        <interface name="management">
            <inet-address value="${jboss.bind.address.management:127.0.0.1}"/>
        </interface>
        <interface name="public">
            <inet-address value="${jboss.bind.address:127.0.0.1}"/>
        </interface>
```
Change these values to something appropriate for your deployment. For instance, the following
configures the management interface to use `0.0.0.0` (listens on any address), and it configures
the public interface to use the system's public IP address. In the default configuration,
these interfaces are only accessible from the local system.
```xml
    <interfaces>
        <interface name="management">
            <inet-address value="${jboss.bind.address.management:0.0.0.0}"/>
        </interface>
        <interface name="public">
            <inet-address value="${jboss.bind.address:171.20.0.10}"/>
        </interface>
```

# Step 6: Create a management user
First, set `JAVA_HOME` and `cd` to the proper directory:
```bash
export JAVA_HOME=/QOpenSys/pkgs/lib/jvm/openjdk-11
cd $WILDFLY/bin
```
Then run the `add-user.sh` script
```bash
add-user.sh
```
Follow these steps:
- When it asks, "What type of user do you wish to add?", enter "a" for management user
- For "Username", enter `admin`
- Enter `a` to choose "a) Update the existing user password and roles"
- Follow the remaining prompts to choose a password

# Step 7: (optional) Download WildFly and place in deployments directory 
```bash
cd $DOWNLOAD
wget https://github.com/gitbucket/gitbucket/releases/download/4.37.1/gitbucket.war
cp gitbucket.war $WILDFLY/standalone/deployments
```
Alternatively, manually download the latest `gitbucket.war` and place in the `standalone/deployments` directory.

Now, the GitBucket application will be deployed when WildFly is started.

# Step 8: Start WildFly

If you configured the server addresses in step 5, you can now start WildFly
in standalone mode by doing the following:
```bash
cd $WILDFLY/bin
standalone.sh
```
If you did not configure the server addresses, you may specify them on the command-line
invocation of `standalone.sh` using the `-b` and `-bmanagement` arguments: 
```bash
cd $WILDFLY/bin
standalone.sh -b 171.20.0.10 -bmanagement 0.0.0.0
```

You're done!! At this point:
- The management interface will be running at `http://<your_server>:9990/` (log in with `admin` and the password you created earlier)
- If you deployed GitBucket in Step 7, it will be running at `http://<your_server>:8080/gitbucket`

If you didn't deploy GitBucket, you can do so through the management interface by doing the following steps:
- Download the latest release of GitBucket from [their releases page on GitHub](https://github.com/gitbucket/gitbucket/releases) (in the form of `gitbucket.war`) to your PC
- Open your browser to `http://<your_server>:9990/` (log in with `admin` and the password you created earlier)
- Click the "Deployments" tab or the "Deployments" link on the homepage
![image](https://user-images.githubusercontent.com/17914061/146619131-3d0d811b-c9fe-4a81-8d80-174c9d7f2a08.png)

- Click the action button in the left sidebar and choose "Upload Deployment"
![image](https://user-images.githubusercontent.com/17914061/146619197-a7b70846-def2-4330-a6a2-fc370a99276f.png)

- Follow the prompts to upload `gitbucket.war` from your PC and specify application names
![image](https://user-images.githubusercontent.com/17914061/146619462-6b254efd-d997-4c10-a731-d6ba78969201.png)

- On success, it should show upload complete
![image](https://user-images.githubusercontent.com/17914061/146619338-69424a55-6695-4536-858d-6a1f39a8d84f.png)

- Once deployed, it will show up in deployments and you can manage through the management console
![image](https://user-images.githubusercontent.com/17914061/146620666-63c8004a-ddd4-4460-8f36-bdd605b19d42.png)

# You should now be running GitBucket with WildFly!
![image](https://user-images.githubusercontent.com/17914061/146620767-e7d2487f-704f-48c4-8125-5836c98bb698.png)


# Managing with Service Commander (optional)
You can elect to manage your WildFly instance with Service Commander. To do so, follow these steps:
- Install the `service-commander` package:
```yum
yum install service-commander
```

- `cd` into your installation's `bin/` directory:
```bash
cd $WILDFLY/bin
```

- Run the `scinit` command. For instance:
```bash
scinit standalone.sh
```
![image](https://user-images.githubusercontent.com/17914061/146621112-a152d72d-f6eb-4733-8c55-2b38a9907d36.png)
It should also print information about where it stored the service definition
![image](https://user-images.githubusercontent.com/17914061/146621169-9c0eef0a-9fcf-47a2-89fd-be48cf349195.png)

Now, you can use the `sc` command to start, stop, or check on your WildFly instance. Examples:
![image](https://user-images.githubusercontent.com/17914061/146621332-d2578c15-ef90-4887-8188-6bfe59d3a2d7.png)



