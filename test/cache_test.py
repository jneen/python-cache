from cache import Cache

class TestCache:
    def __init__(self):
        self._cache = {}

    def set(self, key, val, **kw):
        self._cache[key] = val

    def get(self, key):
        return self._cache.get(key)

def call_counter():
    state = { 'count' : 0 }
    def _call_counter():
        state['count'] += 1
        return state['count']

    return _call_counter


# begin tests
def test_basic():
    backend = TestCache()
    cache = Cache(backend, enabled=True)

    c = cache("counter")(call_counter())

    assert c() == 1 # called the first time
    assert c() == 1 # not called the second time
    assert backend.get("counter")

def test_disable():
    backend = TestCache()
    cache = Cache(backend, enabled=False)

    c = cache("counter")(call_counter())

    assert c() == 1 # called the first time
    assert c() == 2 # called the second time too
    assert not backend.get("counter")

def test_bust():
    backend = TestCache()
    cache = Cache(backend, bust=True)

    c = cache("counter")(call_counter())

    assert c() == 1
    assert c() == 2
    assert backend.get("counter")
