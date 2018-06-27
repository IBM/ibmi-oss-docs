# Summary
Here you will find general information as it relates to Nginx on IBM i.  This is meant to be a supplement to the [official Nginx documentation](https://docs.nginx.com).

# Install

```
$ yum install nginx
```

# Config
The following can be placed in file `/www/nginx/nginx.conf`.
```
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
# Starting and Stopping
To start Nginx you need use use the `/QOpenSys/pkgs/bin/nginx` binary and the `-c` option to declare where the config location.  This is like submitting a job to batch in that it won't lock up your console.

```
$ nginx -c /www/nginx/nginx.conf
```

To stop, run this command.

```
$ nginx -c /www/nginx/nginx.conf -s stop
```
