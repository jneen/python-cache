# cache: caching for humans

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
               and your functions will be run as-is.  This is useful
               for development, when the backend cache may not be
               present at all.
               Default: True

    bust       If `True`, the values in the backend cache will be
               ignored, and new data will be calculated and written
               over the old values.
               Default: False
