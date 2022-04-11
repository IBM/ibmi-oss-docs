# NGINX

```{toctree}
:maxdepth: 1
```

## Summary

Here you will find general information as it relates to Nginx on IBM i.  This is
meant to be a supplement to the [official Nginx documentation](https://docs.nginx.com)
and the wealth of public information available online. Generally speaking, Nginx on IBM i
is managed the same way as on other platforms.

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
base directory. For instance, you can `cd` to the directory where you have your
configuration file and run the following commands to start/stop.
```bash
nginx -p $(pwd) -c $(pwd)/nginx.conf
```
```bash
nginx -p $(pwd) -c $(pwd)/nginx.conf -s stop
```


## HTTP Reverse Proxy (and load balancing)

The below shows how to have Nginx act as a reverse proxy to a Node.js web server
listening on port 49000.  It also redirects port 80 traffic to the secure port
443 (https) which in turn necessitates SSL configuration.
To load-balance across multiple web server, simply add more entries to the
`upstream` block. Note, you may have better performance at scale using a streaming
reverse proxy (see below).

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

### Microcaching

Nginx is also great at caching content. Caching for small durations is sometimes called "microcaching."
This can be particularly useful if your web page or API can tolerate slightly-stale data. For example, 
let's imagine you have an API that runs a database query. Let's say it gets 500 requests per second. 
If you can tolerate data that is 3 seconds "old," then you can enable caching with a 3-second lifespan.
With such a change, you'd go from making 30000 database queries per minute, to only 20 database queries
per minute! Obviously, this is an extreme case, but caching can significantly reduce database load and
improve throughput and response times when used effectively. Note, however, caching has its own
overhead, so it should not be used when a high number of cache misses and a low level of cache hits are
expected. 

The below example illustrates a 5-second microcaching setup, load-balanced across two backend Python
servers.

```nginx
pid nginx.pid;
events {}
http {
  error_log logs/error.log warn;
  proxy_cache_path /tmp/cache keys_zone=cache:10m levels=1:2 inactive=600s max_size=100m;
  upstream python_servers {
    server 127.0.0.1:3341;
    server 127.0.0.1:3342;
  }
  server {
    proxy_cache cache;
    proxy_cache_lock on;
    proxy_cache_valid 200 5s;
    proxy_cache_methods GET HEAD POST;
    proxy_cache_use_stale updating error timeout http_500 http_502 http_503 http_504;
    proxy_buffering on;
    listen 9333 backlog=8096;
    location / {
      proxy_pass http://python_servers;
    }
    location /tablesorter {
      autoindex on;
      alias tablesorter/;
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
can still be handled by the application. You can also combine the `stream` blocks and `http` blocks
into a single configuration. In the below example, nginx will redirect http traffic on port 80 
to https on port 443. On port 443, nginx will handle the TLS encryption and load balance between
three backend servers running on ports 9000, 9001, and 9002.

```nginx
pid nginx.pid;
events {}
stream {
  error_log logs/error.log warn;
  upstream python_servers {
    server 127.0.0.1:9000;
    server 127.0.0.1:9001;
    server 127.0.0.1:9002;
  }
  server {
    ssl_certificate my-cert.pem;
    ssl_certificate_key my-key.pem;
    ssl_protocols TLSv1.2;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-SHA256;
    ssl_session_cache shared:SSL:50m;
    ssl_prefer_server_ciphers on;
    listen 443 ssl backlog=8096;
    proxy_pass python_servers;
  }
}
http {
  server {
    listen 80;
    server_name myserver.com;
    return 301 https://$server_name$request_uri;
  }
}
```
