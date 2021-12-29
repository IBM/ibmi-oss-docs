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

You may choose to download files or deploy TomCat anywhere on the filesystem.
Just change these values accordingly.

(subsequent steps assume you are using this same SSH session)


## Create installation directory and download directory
```bash
mkdir -p $DOWNLOAD
mkdir -p $TOMCAT
```

# Step 1: Install Required Software
```bash
yum install wget tar-gnu gzip nano openjdk-11 ca-certificates-mozilla
```

Alternatively, use Access Client Solutions to install these packages.

# Step 2: Download TomCat

## Technique 1: Using `wget`
(change the version number, if needed, to the version you would like to install)
```bash
cd $DOWNLOAD
wget https://dlcdn.apache.org/tomcat/tomcat-10/v10.0.14/bin/apache-tomcat-10.0.14.tar.gz
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
Create a `setenv.sh` file located in the `/bin` directory of the TomCat installation directory.
This script will be called to set any needed environment variables, and can be used to set `JAVA_HOME`
to the location of our choosing. 
For this, you can use the editor of your choice (assuming you have a drive mapped with sshfs or NetServer),
or you can use a terminal-based editor like nano:
```bash
cd $TOMCAT/bin
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

# Step 5 : Configure server port (optional)
By default, TomCat will listen on port 8080. To change that, open
the `server.xml` file in the `conf/` directory
of the TomCat installation.
For this, you can use the editor of your choice (assuming you have a drive mapped with sshfs or NetServer),
or you can use a terminal-based editor like nano:
```bash
cd $TOMCAT/conf/
nano server.xml
```

Search for `protocol="HTTP` to find the `<Connector>` tag for the HTTP protocol (in nano, this can be
done with ctrl+W). You will find a section that defines which port is used. The `port` value represents
the standard port, and the `redirectPort` is the target port that traffic is redirected to if TLS is required.
```xml
    <Connector executor="tomcatThreadPool"
               port="8080" protocol="HTTP/1.1"
               connectionTimeout="20000"
               redirectPort="8443" />
```
Change these values to something appropriate for your deployment. Also, add `maxPostSize="152428800" to increase
the TomCat maximum file upload size (since GitBucket exceeds the default 50M limit).`For instance, the following
configures the server to use port 9080 for HTTP and port 9443 for TLS:
```xml
    <Connector executor="tomcatThreadPool"
               port="9080" protocol="HTTP/1.1"
               connectionTimeout="20000"
               redirectPort="9443"/>
```
If you changed the redirectPort in the previous step, you will also need to change the connector configuration
for TLS. To do so, search for `protocol="org.apache.coyote` to find the `<Connector>` tag for the TLS protocol
```xml
    <Connector port="8443" protocol="org.apache.coyote.http11.Http11NioProtocol"
               maxThreads="150" SSLEnabled="true">
        <UpgradeProtocol className="org.apache.coyote.http2.Http2Protocol" />
        <SSLHostConfig>
            <Certificate certificateKeystoreFile="conf/localhost-rsa.jks"
                         type="RSA" />
        </SSLHostConfig>
    </Connector>
```
Change as appropriate. In this example, we've changed the `redirectPort` to 9443. For instance:
```xml
    <Connector port="9443" protocol="org.apache.coyote.http11.Http11NioProtocol"
               maxThreads="150" SSLEnabled="true">
        <UpgradeProtocol className="org.apache.coyote.http2.Http2Protocol" />
        <SSLHostConfig>
            <Certificate certificateKeystoreFile="conf/localhost-rsa.jks"
                         type="RSA" />
        </SSLHostConfig>
    </Connector>
```
As you can see, this is also where you would perform the necessary TLS configuration for the server.

# Step 6: Create management users (Optional, recommended)
By default, no user is included in the "manager-gui" role required
to operate the "/manager/html" web application. If you wish to use this app,
you must define such a user in the `tomcat-users.xml` file in the `conf/` directory
of the TomCat installation.
Similarly, there is no user included for "manager-script" role
required to access a plaintext-based management interface, and no "manager-status"
role to see server status

To add these users, you can use the editor of your choice (assuming you have a drive mapped with sshfs or NetServer),
or you can use a terminal-based editor like nano:
```bash
cd $TOMCAT/conf/
nano tomcat-users.xml
```

As an example configuration, you will find a commented-out declaration of `admin` and `root` users, for instance
```xml
<!--
  <user username="admin" password="<must-be-changed>" roles="manager-gui"/>
  <user username="robot" password="<must-be-changed>" roles="manager-script"/>
-->
```
Add the following somewhere inside the `tomcat-users` tag (and outside of a comment), but change the
password value from `admin4ever` to your passwords of choosing.
```xml
  <role rolename="manager-gui"/>
  <role rolename="admin-gui"/>
  <role rolename="manager-script"/>
  <role rolename="manager-status"/>
  <user username="admin" password="admin4ever" roles="admin-gui,manager-gui,manager-script,manager-status"/>
```

# Step 7: Increase TomCat file upload size limit (optional)
TomCat, by default, only lets you upload files that are 50M or smaller. Some large .war files
are larger than this, so it is sometimes good to increase this maximum. 
```bash
cd $TOMCAT/webapps/manager/WEB-INF
nano web.xml
```

Look for the following section:
```xml
    <multipart-config>
      <!-- 50MB max -->
      <max-file-size>52428800</max-file-size>
      <max-request-size>52428800</max-request-size>
      <file-size-threshold>0</file-size-threshold>
    </multipart-config>
```
Change the values of `max-file-size` and `max-request-size` to something larger, like `152428800`.
For instance:
```xml
    <multipart-config>
      <!-- Approx 150MB max -->
      <max-file-size>152428800</max-file-size>
      <max-request-size>152428800</max-request-size>
      <file-size-threshold>0</file-size-threshold>
    </multipart-config>
```



# Step 8: Convert GitBucket to Jakarta EE and Deploy

GitBucket is built against Java EE. However, TomCat 10 (used in this guide) now uses Jakarta EE
classes. See [the relevant TomCat docs](https://tomcat.apache.org/migration-10.html)) for more
information. There is a TomCat migration tool available, but TomCat can also automatically
convert applications on startup. To do so, place the `.war` in the `webapps-javaee` directory:

```bash
cd $DOWNLOAD
wget https://github.com/gitbucket/gitbucket/releases/download/4.37.1/gitbucket.war
mkdir -p $TOMCAT/webapps-javaee
cp gitbucket.war $TOMCAT/webapps-javaee
```

# Step 9: Start TomCat
```bash
cd $TOMCAT/bin
./startup.sh
```
You're done!! At this point:
- Tomcat should now be running at `http://<server_name>:8080` (or whatever port you've chosen earlier).
- GitBucket should now be running at `http://<server_name>:8080/gitbucket` (or whatever port you've chosen earlier)


You can deploy other applications through the management interface by doing the following steps:
- Open your browser to `http://<your_server>:8080/`
- Click the "Manager App" button (log in with `admin` and the password you created earlier)
![image](https://user-images.githubusercontent.com/17914061/147600657-28dacbc2-be14-459d-ac7f-0f84170497ba.png)

- Scroll down to the "Deploy" section and go to "WAR file to deploy". Browse for your `gitbucket.war` file and
click "Deploy"
![image](https://user-images.githubusercontent.com/17914061/147600763-4f7f8faf-46ec-4c14-8f7b-0754a13c89e7.png)

- You should now see your application in the deployed application list and can start/stop/etc through this interface.

# Step 10: Managing with Service Commander (optional)
You can elect to manage your WildFly instance with Service Commander. If you are unfamiliar with Service Commander,
you can read more [here](https://theprez.github.io/ServiceCommander-IBMi/#service-commander-for-ibm-i). 
The steps to leverage this tool include:
- Install the `service-commander` package:
```yum
yum install service-commander
```

- `cd` into your installation's `bin/` directory:
```bash
cd $TOMCAT/bin
```

- Run the `scinit` command to create a service definition for the `startup.sh` command. Proceed to answer
the questions as in the following screenshot, except use the port number you chose earlier (and feel free to 
use name as you wish). 
If you configured the server addresses in step 5:
```bash
scinit ./startup.sh
```
![image](https://user-images.githubusercontent.com/17914061/147699367-ab8eef45-4103-450a-9162-de8030c2edfc.png)

It should also print information about where it stored the service definition
![image](https://user-images.githubusercontent.com/17914061/147699504-84de2cd8-85bc-4452-bb45-e13483a80a24.png)

Now, you can use the `sc` command to start, stop, or check on your WildFly instance. Examples:
![image](https://user-images.githubusercontent.com/17914061/147699566-29274c08-49b2-4416-81e0-246c7a92144d.png)


