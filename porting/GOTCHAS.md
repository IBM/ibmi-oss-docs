# Gotchas When Building Software in PASE

```{toctree}
:maxdepth: 1
```

## malloc behaves differently from many other platforms

[Zero byte allocations](https://whatilearned2day.wordpress.com/2006/07/13/zero-sized-allocation-using-malloc-on-aix/)
on AIX can be strange. If software depends on this behaviour, you can build with
`-D_LINUX_SOURCE_COMPAT` to enable a built-into-libc wrapper that has the glibc behaviour.

## C++ issues

Make sure that you have `libstdcplusplus-devel` in addition to g++ installed.

If you run into issues with the threading parts of the C++ standard library,
such as `std::mutex`, ensure that `-pthread` is passed to g++. This will flip
some defines and such so that threading is exposed. Linking pthread (`-pthread`
if you use GCC as the linker, otherwise `-lpthread`) in also helps with crashes
in C++ standard library locale code.

## AF_LOCAL not declared

```text
error: 'AF_LOCAL' was not declared in this scope
     c = socket(AF_LOCAL, SOCK_STREAM, 0);
                ^~~~~~~~
```

On some platforms, `AF_LOCAL` is provided as a synonym of `AF_UNIX`, but not on
AIX/PASE. Either alter the code to use `AF_UNIX` directly or add your own synonym:

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

Understanding the TOC (table of contents) could take up its own entire article.
Indeed there's a good one [here](https://www.ibm.com/developerworks/rational/library/overview-toc-aix/index.html).
The usual way to fix is by passing `-bbigtoc` option to the linker (`ld`).
Using GCC, you need to prefix linker flags with `-Wl,` and these flags are
specified in `$LDFLAGS`:

```bash
export LDFLAGS='-Wl,-bbigtoc'
./configure ...
make ...
```

While `-bbigtoc` should always do the job, it's not the most efficient. GCC also
has additional ways to reduce TOC pressure that may be better performing, but
you'll need to understand the code you're trying to compile and what each option
does to apply them. Look for more info on the following compiler options [here](https://gcc.gnu.org/onlinedocs/gcc/RS_002f6000-and-PowerPC-Options.html#RS_002f6000-and-PowerPC-Options):

- `-mno-fp-in-toc`
- `-mno-sum-in-toc`
- `-mminimal-toc`
- `-mcmodel=medium`
- `-mcmodel=large`

## `readdir_r` return values

On AIX and PASE, `readdir_r` returns 9 and sets the result to NULL for both end
of directory and error; on error, it sets `errno`. This is unlike other Unix
systens and very easy to use incorrectly even when adapting to its quirks, so
you can try:

- Set `errno` to 0 before calling. This means you can disambiguate between the cases.
- Build with `-D_LINUX_SOURCE_COMPAT`. This will point `readdir_r` to an
alternative version with glibc-like semantics.

## `uname` return values

Mostly a cosmetic issue, but applications expecting a full version in the
release field of utsname will be disappointed. AIX and PASE put the major
version (you know, the "V" in "V7R3") in version, and the minor version (the
"R") in release.

## Thread safety

AIX and PASE are **not** thread safe by default. You should pass
`-D_THREAD_SAFE`, which enables important things like a thread-safe `errno`.

## VFS woes

`mntctl`, `statvfs`, and ILE `statvfs` can never agree on a consistent value for
magic names and numbers, unlike AIX. Try to avoid converting between their values.

## SIOCGIFCONF

On PASE, `SIOCGIFCONF` doesn't show the true line description name, nor does it
return an `AF_LINK` entry; the device will have a fake name based on its IPv4 address.
This makes getting the interface index and MAC address nearly impossible; you
can't even use `if_nameindex` because that returns the true line description name.
As an alternative, you can use `Qp2getifaddrs`, which works like most Unix-like
systems' `getifaddrs`.
