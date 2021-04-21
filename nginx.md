# NGINX

## Summary

Here you will find general information as it relates to Nginx on IBM i.  This is
meant to be a supplement to the [official Nginx documentation](https://docs.nginx.com).

## Install

```bash
yum install nginx
```

## Config

The following can be placed in file `/www/nginx/nginx.conf`.

```nginx configuration file
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

## Reverse Proxy

The below shows how to have Nginx act as a reverse proxy to a Node.js web server
listening on port 49000.  It also redirects port 80 traffic to the secure port
443 (https) which in turn necessitates SSL configuration.

```nginx configuration file

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
