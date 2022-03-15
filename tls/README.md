# TLS Setup

```{toctree}
:maxdepth: 1
```

## Best practices

It is often considered best practice to not handle TLS encryption within the application (for
instance, your Node.js or Python aplication).
Instead, handle the TLS setup in a separate HTTP server that runs in front of your application.
The two most reasonable options for this are NGINX and Apache (IBM i HTTP server).

You may choose to use [LetsEncrypt and/or CertBot](../certbot.md) to generate production-ready
certificates.

## Creating a self-signed certificate

Run the following steps to generate a self-signed certificate for development (not production):

```openssl
openssl genrsa -out my-key.pem 2048
openssl req -new -sha256 -key my-key.pem -out my-csr.pem
openssl x509 -req -in my-csr.pem -signkey my-key.pem -out my-cert.pem
```

## Setting up TLS with NGINX (uses OpenSSL)

See [the NGINX notes](../nginx.md).

## Setting up IBM i HTTP Server (uses Digital Certificate Manager)

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
