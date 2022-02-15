# TLS Setup

## Best practices

It is often considered best practice to not handle TLS encryption within the application (for
instance, your Node.js or Python aplication).
Instead, handle the TLS setup in a separate HTTP server that runs in front of your application.
The two most reasonable options for this are NGINX and Apache (IBM i HTTP server).

### Setting up TLS with NGINX (uses OpenSSL)

See [the NGINX notes](../nginx.md).

### Setting up IBM i HTTP Server (uses Digital Certificate Manager)

See [this article on MC Press Online](https://www.mcpressonline.com/operating-systems/ibm-i-os400-i5os/using-apache-as-a-reverse-proxy-on-ibm-i)
for information on using IBM i HTTP Server (Apache) as a reverse proxy. Then,
simply configure TLS as you would for other IBM i servers in Digital Certificate
Manager (DCM). See [this IBM support document](https://www.ibm.com/support/pages/digital-certificate-manager-dcm-frequently-asked-questions-and-common-tasks),
particularly the "How do I configure an HTTP server for SSL?" section for more information on
the steps needed to configure DCM.

## Want to handle TLS in the application anyway?

If you still wish to handle TLS in the application (perhaps for development purposes), be aware that:
- Configuration for the IBM i will generally be the same as on other platforms.
- Digital Certificate Manager (DCM) is not used (you can, however, export the certificate from DCM for
use with your application).

So, for example, when configuring a Node.js server for TLS, you can reference the
[Node.js documentation on HTTPS](https://nodejs.org/api/https.html). If using a web framework, that
framework's documentation will often have useful information and examples. 
