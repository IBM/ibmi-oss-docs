# Gotchas When Building Software in PASE

## AF_LOCAL not declared

```text
error: 'AF_LOCAL' was not declared in this scope
     c = socket(AF_LOCAL, SOCK_STREAM, 0);
                ^~~~~~~~
```

On some platforms, `AF_LOCAL` is provided as a synonym of `AF_UNIX`, but not on AIX/PASE. Either alter the code to use `AF_UNIX` directly or add your own synonym:

```C
#ifndef AF_LOCAL
#define AF_LOCAL AF_UNIX
#endif

// ...
c = socket(AF_LOCAL, SOCK_STREAM, 0);
```
