# TLS Setup

## Best practices

It is often considered best practice to not handle TLS encryption within the application.
Instead, handle the TLS setup in a separate HTTP server that runs in front of your application.
The two most reasonable options for this are NGINX and Apache (IBM i HTTP server).

### Setting up TLS with NGINX (uses OpenSSL)

See [the NGINX notes](../nginx.md).

### Setting up IBM i HTTP Server (uses Digital Certificate Manager)

See [this article on MC Press Online](https://www.mcpressonline.com/operating-systems/ibm-i-os400-i5os/using-apache-as-a-reverse-proxy-on-ibm-i)
for information on using IBM i HTTP Server (Apache) as a reverse proxy. Then,
simply configure TLS as you would for other IBM i servers in Digital Certificate
Manager (DCM).