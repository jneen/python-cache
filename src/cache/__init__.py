# local dependencies
from .version import __version__

# external dependencies
from decorator import decorator

# stdlib
from inspect import getargspec

class Cache:
    DEFAULT_OPTIONS = {
        'enabled': True
    }

    def __init__(self, backend, **default_options):
        self.backend = backend
        self.default_options = self.DEFAULT_OPTIONS.copy()
        self.default_options.update(default_options)

    def __call__(self, key, **kw):
        opts = self.default_options.copy()
        opts.update(kw)

        def _cache(fn):
            return CacheWrapper(self.backend, key, fn, **opts)

        return _cache

class CacheWrapper:
    def __init__(self, backend, key, calculate, **kw):
        self.backend = backend
        self.key = key
        self.calculate = calculate
        self.options = kw

        if len(getargspec(calculate).args) > 0:
            raise TypeError("cannot cache a function with arguments")

    def cached(self, default='__absent__'):
        cached = None
        if self.options.get('enabled') and not self.options.get('bust'):
            cached = self.backend.get(self.key)

        if cached is None:
            if default == '__absent__':
                raise KeyError

            return default

        return self._unprepare_value(cached)

    def _prepare_value(self, value):
        return { 'value': value }

    def _unprepare_value(self, prepared):
        return prepared['value']

    def refresh(self):
        fresh = self.calculate()
        if self.options.get('enabled'):
            value = self._prepare_value(fresh)
            self.backend.set(self.key, value, **self.options)

        return fresh

    def get(self):
        try:
            return self.cached()
        except KeyError:
            return self.refresh()

    def __call__(self):
        return self.get()
