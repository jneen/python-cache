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
