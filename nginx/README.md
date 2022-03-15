# NGINX

```{toctree}
:maxdepth: 1
```

## Summary

Here you will find general information as it relates to Nginx on IBM i.  This is
meant to be a supplement to the [official Nginx documentation](https://docs.nginx.com).

As outlined in [the Apache documentation](../apache/README.md), there are several advantages
to using an HTTP server in front of your application. It is not good practice to serve up
directly from a framework or application server in production.

**Of note: Apache (IBM HTTP Server for i) uses Digital Certificate Manager (DCM) to configure
TLS. Nginx uses standard OpenSSL technology**

## Install

```bash
yum install nginx
```

## Simple static HTML server example

The following can be placed in file `/www/nginx/nginx.conf`.

```nginx
pid /www/nginx/nginx.pid;
events {}
http {
  server {
    listen       8001;
    server_name  localhost;
    location / {
      root   /www/nginx/html;
      index  index.html;
    }
  }
}
```

## Starting and Stopping

To start Nginx you need use use the `/QOpenSys/pkgs/bin/nginx` binary and the
`-c` option to declare where the config location.  This is like submitting a job
to batch in that it won't lock up your console.

```bash
nginx -c /www/nginx/nginx.conf
```

To stop, run this command.

```bash
nginx -c /www/nginx/nginx.conf -s stop
```

You can also use the `-p` option to set the base directory. This allows relative
path names in the configuration (pid file, logs, etc) to be resolved relative to the
base directory. 
```bash
nginx -p /www/nginx -c /www/nginx/nginx.conf
```
```bash
nginx -p /www/nginx -c /www/nginx/nginx.conf -s stop
```


## HTTP Reverse Proxy (and load balancing)

The below shows how to have Nginx act as a reverse proxy to a Node.js web server
listening on port 49000.  It also redirects port 80 traffic to the secure port
443 (https) which in turn necessitates SSL configuration.
To load-balance across multiple web server, simply add more entries to the
`upstream` block.

```nginx
pid /www/mydomain/nginx.pid;
events {}
http {
  server {
    listen 80;
    server_name mydomain.com;
    return 301 https://$server_name$request_uri;
  }
  upstream node_servers {
    server 127.0.0.1:49000;  
  }
  server {
    listen 443 ssl;
    ssl on;
    ssl_certificate /www/mydomain/mydomain.com.cert;
    ssl_certificate_key /www/mydomain/mydomain.com.key;
    ssl_protocols TLSv1.2;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-SHA256
    ssl_session_cache shared:SSL:50m;
    ssl_prefer_server_ciphers on;
    location / {
      proxy_pass http://node_servers;
    }
  }
}
```

## Streaming Reverse Proxy (and load balancing)

Nginx also supports stream-based proxying and load balancing. This can work for many protocols
(not just http) and consumes less overhead than an HTTP reverse proxy. However, since it doesn't
do any HTTP-specific operations, it doesn't support any http-specific concepts (like HTTP redirects,
header filtering/rewriting, "sticky" sessions, etc). The below shows how to load-balance across
three backend servers running on ports 9000, 9001, and 9002. Note the relative paths for the
pid file and error logs, so this configuration should be started with the `-p` option as shown above.

```nginx
pid nginx.pid;
events {}
stream {
  error_log logs/error.log warn;
  upstream node_servers {
    server 127.0.0.1:9000;
    server 127.0.0.1:9001;
    server 127.0.0.1:9002;
  }
  server {
    listen 80 backlog=8096;
      proxy_pass node_servers;
  }
}
```

Of note, the ssl directives can still be used with a streaming reverse proxy. Also, http concepts
can still be handled by the application. For instance, you could run a simple HTTP server that redirects
from port 80 to port 443 and proxy to it. For instance:

```nginx
pid nginx.pid;
events {}
stream {
  error_log logs/error.log warn;
  upstream node_servers {
    server 127.0.0.1:9000;
    server 127.0.0.1:9001;
    server 127.0.0.1:9002;
  }
  server {
    listen 443 backlog=8096;
    proxy_pass node_servers;
  }
  upstream redirect_server {
    server 127.0.0.1:8999;
  }
  server {
    listen 80 backlog=8096;
    proxy_pass redirect_server;
  }
}
```
