# Known Issues

```{toctree}
:maxdepth: 1
```

## [fs.watch](https://nodejs.org/api/fs.html#fswatchfilename-options-listener)

On IBM i systems, this feature is not supported.

This is also documented in the [caveats](https://nodejs.org/api/fs.html#caveats)
section of the `fs.watch` documentation.

When using various Node.js tools for watching a filesystem and hot-reloading on
file changes, many use Chokidar which relies on fs.watch, which is not supported
on IBM i. This results in error messages such as:

```text
Watchpack Error (watrcher): Error: ENONSYS: function not implmemented, watch
Error from chokidar src/api/modules): error enosys: function not implemented, watch
```

As a workaround, Chokidar supports polling, which can be enabled by setting the 
`CHOKIDAR_USEPOLLING` environment variable to 1.

As of `chokidar >= 3.5.2`, the default is to use polling on IBM i and it should
work out of the box.

As of `nodemon >= 3.0.1`, the default is to use polling on IBM i and it should
work out of the box.

## [os.uptime](https://nodejs.org/api/os.html#osuptime)

On IBM i systems, this feature is not supported.
Calling `os.uptime` returns a system error `ENOSYS`.
