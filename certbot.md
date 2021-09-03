# LetsEncrypt w/Certbot
Certbot can be used to get/renew LetsEncrypt certificates. Follow these instructions to install and use Certbot. 
Certbot's web site can be found at [https://certbot.eff.org](https://certbot.eff.org).

## 1. SSH into the server

SSH into the server running your HTTP website as a user with *ALLOBJ special authority.

## 2. Set up your environment

It is assumed that you are running these commands from an SSH terminal.

You must first assure that your PATH environment variable is set up correctly.
```
    PATH=/QOpenSys/pkgs/bin:$PATH
    export PATH
```

## 3. Install system dependencies

Install Python 3.9 and necessary packages by running:
```
yum install python39-pip python39-cryptography
```

## 4. Set up a Python virtual environment

Execute the following instruction on the command line to set up a virtual environment.
```
python3.9 -m venv --system-site-packages /opt/certbot
```

## 5. Install Certbot

Run this command on the command line on the machine to install Certbot.
```
/opt/certbot/bin/pip install certbot
```

## 6. Choose how you'd like to run Certbot

### Are you ok with temporarily stopping your website?
#### Yes, my web server is not currently running on this machine.

Stop your webserver, then run this command to get a certificate. Certbot will temporarily spin up a webserver on your machine.
```
/opt/certbot/bin/certbot certonly --standalone
```

#### No, I need to keep my web server running.

If you have a webserver that's already using port 80 and don't want to stop it while Certbot runs, run this command and follow the instructions in the terminal.
```
/opt/certbot/bin/certbot certonly --webroot
```

##### Important Note:

To use the webroot plugin, your server must be configured to serve files from hidden directories. If /.well-known is treated specially by your webserver configuration, you might need to modify the configuration to ensure that files inside /.well-known/acme-challenge are served by the webserver.

## 7. Install your certificate

Proper technique will vary depending on the web server in use. If using IBM i system Apache, [the DCM Tools project](https://github.com/ThePrez/DCM-tools/) may be useful.

## 8. Confirm that Certbot worked

To confirm that your site is set up properly, visit https://yourwebsite.com/ in your browser and look for the lock icon in the URL bar. Most browsers will also let you inspect the certificate by clicking on the lock icon.

## 9. Renewing your certificate manually

Certificate renewal can be done by running the following in your terminal:

    /opt/certbot/bin/certbot renew

You can do a "dry run" of the renewal (making no modifications) by running:

/opt/certbot/bin/certbot renew --dry-run

## 10. Setting up automatic renewal

To set up automatic renewal of your certificate, first create a shell script that performs the following tasks:
- Stops your web server
- Runs /opt/certbot/bin/certbot renew -q
- Installs the certificate
- Starts your web server
- (optional) Records the activity, for instance by running `system "SNDMSG MSG('Certificate renewal process complete') TOUSR(*SYSOPR)"`

Once that is completed, you can create a job scheduler entry. This example Shows how to create a job scheduler entry that runs at 1:11 AM on the first and third sundays.
```
ADDJOBSCDE JOB(CERTRENEW) CMD(QSH CMD('/path/to/script.sh')) FRQ(*MONTHLY) SCDDATE(*NONE) SCDDAY(*SUN) SCDTIME(011111) RELDAYMON(1 3) SAVE(*YES)
```
Replace the job name and path to script as needed.

## 11. Upgrading Certbot

It's good practice to occasionally update Certbot to keep it up-to-date. To do this, run the following command on the command line on the machine.
```
/opt/certbot/bin/pip install --upgrade certbot
```

If this step leads to errors, run `rm -rf /opt/certbot` and repeat all installation instructions.







## What about wildcard certificates?

If you need wildcard certificates, follow steps 1-5, above, then proceed as documented here

### 6. Check if your DNS provider is supported

See if your DNS provider is supported by Certbot by checking [this list in the documentation](https://certbot.eff.org/docs/using.html#dns-plugins).

#### Not supported?

If your DNS provider is not supported, pause here: run Certbot with the manual plugin by using [these steps from the documentation](https://certbot.eff.org/docs/using.html#manual).

##### Supported?

If your DNS provider is supported, continue with the remaining instructions below in your SSH terminal.

### 7. Install correct DNS plugin

Run the following command, replacing <PLUGIN> with the name of your DNS provider.
```
/opt/certbot/bin/pip install certbot-dns-<PLUGIN>
```
For example, if your DNS provider is Cloudflare, you'd run the following command:
```
/opt/certbot/bin/pip install certbot-dns-cloudflare
```

### 8. Set up credentials

You'll need to set up DNS credentials.
Follow the steps in the "Credentials" section for your DNS provider to access or create the appropriate credential configuration file. Find credentials instructions for your DNS provider by clicking [the DNS plugin's name on the Documentation list](https://certbot.eff.org/docs/using.html#dns-plugins).

### 9. Get a certificate

Run one of the commands in the "Examples" section of the [instructions for your DNS provider](https://certbot.eff.org/docs/using.html#dns-plugins).

### 10. Install and renew certificate

Follow steps 7 and beyond, above. 
