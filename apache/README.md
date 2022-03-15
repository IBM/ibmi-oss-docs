# Integrating with Apache (IBM HTTP Server for i)

```{toctree}
:maxdepth: 1
```

## Why?

It is often recommended that you host web applications and APIs behind an HTTP server such
as Nginx or Apache. On IBM i, Nginx is available as a PASE RPM. Apache is provided as
part of the IBM HTTP Server for i (5770-DG1) product. 

The HTTP server can handle many things to help make your application production-ready, for
instance:

- queuing connections when under heavy load
- Handling TLS. Note that HTTP Server for i integrates with Digital Certificate Manager (DCM),
whereas Nginx does not.
- Filtering various HTTP headers, etc.
- Handling authentication
- Serving static content (often more efficiently than a high-level language application server)
- Handling multiple languages/applications behind a single virtual host
- Provide logging of HTTP requests

This document offers basic insight into how to tie open source workloads to Apache. It is
assumed that you have a basic knowledge of some concepts.

You may also want to consider using [Nginx](../nginx/README.md)!

## Technique # 1: ProxyPass directives

The Apache HTTP server can serve as a simple reverse proxy to any other HTTP server,
regardless of how that HTTP server is implemented.

To do this, your `httpd.conf` needs to load the needed proxy modules. Unlike other platforms,
which ship `.so` files (like `mod_proxy.so`), the extensions on IBM i are built in
ILE service program form. 

```apache
LoadModule proxy_module         /QSYS.LIB/QHTTPSVR.LIB/QZSRCORE.SRVPGM
LoadModule proxy_http_module    /QSYS.LIB/QHTTPSVR.LIB/QZSRCORE.SRVPGM
LoadModule proxy_connect_module /QSYS.LIB/QHTTPSVR.LIB/QZSRCORE.SRVPGM
```

Once those modules are loaded, you can use the `ProxyPass` and `ProxyPassReverse` directives
to forward the traffic to a backend server. For instance, if you have a Python/Node.js application
running on localhost port 8000, you can forward the traffic with these directives:

```apache
ProxyPass         / http://localhost:8000/
ProxyPassReverse  / http://localhost:8000/
```
These directives can also be used for specific pathis within the website. For instnace,
to forward requests from within `/site`:

```apache
ProxyPass         /site/  http://localhost:8000/site/
ProxyPassReverse  /site/  http://localhost:8000/site/
``` 

When using this approach, you need to manage the backend job separately from the Apache instance.
That is, a `STRTCPSVR` will not automatically start the backend jobs. Optionally, you can use
[Service Commander](https://theprez.github.io/ServiceCommander-IBMi/#service-commander-for-ibm-i)
for a more unified experience.

Using a reverse proxy approach is generally best practice for non-PHP languages, because:
- You can still leverage other open source tools to handle multiple processes if needed. Examples include:
  - `pm2`
  - `uvicorn` or `hypercorn` (Python)
  - `gunicorn` (Python)
- You can generally choose any application server or web framework you like. There are many to choose from!
Application servers that are optimized for a specific language tend to scale well. 
- It is relatively easy to configure and troubleshoot, even if you have little to no Apache experience.

## Technique # 2: FastCGI

FastCGI in Apache is powered by the "Zend enabler." While originally written to support PHP workloads,
it can work for any language that is aware of the FastCGI protocol. 

To use FastCGI, first load the Zend enabler module:

```apache
LoadModule zend_enabler_module /QSYS.LIB/QHTTPSVR.LIB/QZFAST.SRVPGM
```

If you'd like to run under a different user ID, you can also use the `FastCGIServerID` and
`ServerUserID` directives to specify an alternative profile. `ServerUserID` affects the core Apache
operations (for instance, serving static files), and `FastCGIServerID` affects the processes
launched by the Zend enabler.
```apache
ServerUserID JGORZINS
FastCGIServerID JGORZINS
```

Next, you will add a `<Directory>` specification, where you add a type and handler for a particular
URL path extension. In this case, I specify that all requests with a `.js` extension are handled
by handler `fastcgi-script` (the Zend enabler module) with type `application/x-httpd-js`
```apache
<Directory /www/myserver/htdocs/>
  order allow,deny
  allow from all
  AddType application/x-httpd-js .js
  AddHandler fastcgi-script .js
</Directory>
```

You must also define the type in the Zend enabler modeule by way of the `fastcgi.conf` configuration file. 
You must specify `Server type` and `CommandLine`. You can also use `StartProcesses` to start multiple backend
jobs. The `SetEnv` directive is also commonly-used.
The `IpcDir` and `IpcPublic` directives are also needed for setting the behavior of UNIX Domain sockets
```lisp
; node.js server
Server type="application/x-httpd-js" CommandLine="/www/myserver/htdocs/node/index.js" StartProcesses="4"  SetEnv="LC_ALL=EN_US.UTF-8" 
; Where to place socket files
IpcDir /www/myserver/logs
IpcPublic *RWX
```

You will also need to place a proper "shebang" (`#!`) line at the beginning of your script to run the proper executable.
For instance, the first line of your `index.js` could be `#!/QOpenSys/pkgs/bin/node`.

With FastCGI, the backend worker jobs are managed by Apache, so `STRTCPSVR` and `ENDTCPSVR` commands also
start/stop the worker backend jobs as needed.

FastCGI is best practice when using PHP. PHP has a long history with the FastCGI protocol, and they have evolved to work
together very well.

## Technique # 3: CGI (not recommended)

CGI is one of the oldest techniques for integrating code with an HTTP server. Since it just uses the standard in/out
of a process to serve an HTTP request, it is truly language-agnostic.
However, it is generally not recommended for use with open source languages, because:
- It is inefficient (spawns a job for every request). Slow performance and high CPU usage is expected
- There are very few frameworks that support CGI. Those projects, generally speaking, are "abandonware"
and no longer maintained.
See [this doc](http://www.youngiprofessionals.com/wiki/index.php/PASE/PASECGI), which may be out of date, for possible guidance.
