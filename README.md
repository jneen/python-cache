# cache: caching for humans

## Installation

    pip install cache

## Usage:

``` python
import pylibmc
from cache import Cache

backend = pylibmc.Client(["127.0.0.1"])

cache = Cache(backend)

@cache("mykey")
def some_expensive_method():
    sleep(10)
    return 42

# writes 42 to the cache
some_expensive_method()

# reads 42 from the cache
some_expensive_method()

# re-calculates and writes 42 to the cache
some_expensive_method.refresh()

# get the cached value or throw an error
some_expensive_method.cached()

# get the cached value or return 3
some_expensive_method.cached(default=3)
```

## Options

Options can be passed to either the `Cache` constructor or the decorator.  Options passed to the decorator take precedence.  Available options are:

    enabled    If `False`, the backend cache will not be used at all,
               and your functions will be run as-is, even when you call
               `.cached()`.  This is useful for development, when the
               function may be changing rapidly.
               Default: True

    bust       If `True`, the values in the backend cache will be
               ignored, and new data will be calculated and written
               over the old values.
               Default: False

The remaining options, if given, will be passed as keyword arguments to the backend's `set` method.  This is useful for things like expiration times - for example, using pylibmc:

``` python
@cache("some_key", time=1000)
def expensive_method():
    # ...
```

## Local Caches

Cache provides two "fake" caches for local development without a backend cache: `LocalCache` and `NullCache`.  `LocalCache` uses a dictionary in place of a backend cache, and `NullCache` is a noop on `set` and always returns `None` on `get`.

The difference between passing `enabled=False` to the cache and using `NullCache` comes in when you use the `.cached()` method.  If the cache is disabled, `.cached()` will run the underlying function, but `NullCache` will throw a `KeyError` as if the key was not present.

### P.S.

If you're a Ruby user, check out the analogous [Cacher][] library for Ruby

[Cacher]: https://github.com/jayferd/cacher
