from cache import Cache, LocalCache, NullCache


def call_counter():
    state = {'count': 0}

    def _call_counter():
        state['count'] += 1
        return state['count']

    return _call_counter


# begin tests
def test_basic():
    backend = LocalCache()
    cache = Cache(backend, enabled=True)

    c = cache("counter")(call_counter())

    assert c() == 1, 'called the first time'
    assert c() == 1, 'not called the second time'
    assert c.refresh() == 2
    assert backend.get("counter")


def test_disable():
    backend = LocalCache()
    cache = Cache(backend, enabled=False)

    c = cache("counter")(call_counter())

    assert c() == 1, 'called the first time'
    assert c() == 2, 'called the second time too'
    assert c.cached() == 3, 'called even when you get the cached val'
    assert not backend.get("counter")


def test_bust():
    backend = LocalCache()
    cache = Cache(backend, bust=True)

    c = cache("counter")(call_counter())

    assert c() == 1
    assert c() == 2
    assert c.cached() == 2, 'not called if you just get the cached val'
    assert backend.get("counter")


def test_null():
    backend = NullCache()
    cache = Cache(backend)

    c = cache("counter")(call_counter())

    assert c() == 1
    assert c() == 2
    assert c.cached(default=42) == 42
    try:
        c.cached()
        assert False, 'should raise an error'
    except KeyError:
        pass

    assert not backend.get("counter")
