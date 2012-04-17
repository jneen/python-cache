from cache import Cache, LocalCache, NullCache


class CallCounter:
    def __init__(self):
        self.count = 0

    def __call__(self):
        self.count += 1
        return self.count


# begin tests
def test_basic():
    backend = LocalCache()
    cache = Cache(backend, enabled=True)

    c = cache("counter")(CallCounter())

    assert c() == 1, 'called the first time'
    assert c() == 1, 'not called the second time'
    assert c.refresh() == 2
    assert backend.get("counter")


def test_disable():
    backend = LocalCache()
    cache = Cache(backend, enabled=False)

    c = cache("counter")(CallCounter())

    assert c() == 1, 'called the first time'
    assert c() == 2, 'called the second time too'
    assert c.cached() == 3, 'called even when you get the cached val'
    assert not backend.get("counter")


def test_bust():
    backend = LocalCache()
    cache = Cache(backend, bust=True)

    c = cache("counter")(CallCounter())

    assert c() == 1
    assert c() == 2
    assert c.cached() == 2, 'not called if you just get the cached val'
    assert backend.get("counter")


def test_null():
    backend = NullCache()
    cache = Cache(backend)

    c = cache("counter")(CallCounter())

    assert c() == 1
    assert c() == 2
    assert c.cached(default=42) == 42
    try:
        c.cached()
        assert False, 'should raise an error'
    except KeyError:
        pass

    assert not backend.get("counter")


def test_key_default():
    backend = LocalCache
    cache = Cache(backend)

    @cache()
    def some_method_name():
        return 1

    assert some_method_name.key == '<cache>/some_method_name'


def test_arguments():
    backend = LocalCache()
    cache = Cache(backend)

    @cache("mykey")
    def expensive(*a, **kw):
        pass

    expensive(1, foo=2)
    expensive(1, foo=2)

    keys = backend._cache.keys()

    assert len(keys) == 1, "only one key is set"
    assert ("mykey/args:") in keys[0]
