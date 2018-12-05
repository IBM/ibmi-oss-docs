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

## TOC overflow

```text
ld: 0711-781 ERROR: TOC overflow. TOC size: 85080       Maximum size: 65536
collect2: error: ld returned 12 exit status
```

Understanding the TOC (table of contents) could take up its own entire article. Indeed there's a good one [here](https://www.ibm.com/developerworks/rational/library/overview-toc-aix/index.html). The usual way to fix is by passing `-bbigtoc` option to the linker (`ld`). Using GCC, you need to prefix linker flags with `-Wl,` and these flags are specified in `$LDFLAGS`:

```bash
export LDFLAGS='-Wl,-bbigtoc'
./configure ...
make ...
```

While `-bbigtoc` should always do the job, it's not the most efficient. GCC also has additional ways to reduce TOC pressure that may be better performing, but you'll need to understand the code you're trying to compile and what each option does to apply them. Look for more info on the following compiler options [here](https://gcc.gnu.org/onlinedocs/gcc/RS_002f6000-and-PowerPC-Options.html#RS_002f6000-and-PowerPC-Options):

- `-mno-fp-in-toc`
- `-mno-sum-in-toc`
- `-mminimal-toc`
- `-mcmodel=medium`
- `-mcmodel=large`
