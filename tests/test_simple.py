from pytest_redis import factories
from retask import Queue

from port_for import get_port
port = get_port(None)
if not isinstance(port, int):
    port = 6666
rp = factories.redis_proc(port=port)

redis_my = factories.redisdb('rp')

def test_first(redis_my):
    q = Queue("testqueue", config={"port": port})
    assert q.connect()

