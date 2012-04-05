from decorator import decorator
from time import sleep
from inspect import getargspec

from .version import VERSION

class TestCache:
    def __init__(self):
        self._cache = {}

    def set(self, key, val, **kw):
        self._cache[key] = val

    def get(self, key):
        return self._cache.get(key)

class Cache:
    def __init__(self, cache):
        self.cache = cache

    def __call__(self, key, **kw):
        def _cache(fn):
            return CacheWrapper(self.cache, key, fn, **kw)

        return _cache

class CacheWrapper:
    def __init__(self, cache, key, calculate, **kw):
        self.cache = cache
        self.key = key
        self.calculate = calculate
        self.options = kw

        if len(getargspec(calculate).args) > 0:
            raise TypeError("cannot cache a function with arguments")

    def cached(self, default='__absent__'):
        cached = self.cache.get(self.key)
        if cached is None:
            if default == '__absent__':
                raise KeyError

            return default

        return cached

    def refresh(self, *args, **kwargs):
        fresh = self.calculate(*args, **kwargs)
        self.cache.set(self.key, fresh, **self.options)
        return fresh

    def conditionally_calculate(self, *args, **kwargs):
        try:
            return self.cached()
        except KeyError:
            return self.refresh(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.conditionally_calculate(*args, **kwargs)


if __name__ == '__main__':
    cache = Cache(TestCache())

    @cache("my_cache/expensive", ttl=100)
    def expensive():
        print "===== calculating ====="
        return "done."

    expensive.cached(default=3)
    expensive.refresh()
