from pynode.store.inmemorystore import InMemoryStore
from pynode.store.mysqlstore import MysqlStore
from pynode.store.store import Store

async def mysql() -> Store:
    return await MysqlStore.gen()

async def inmemory() -> Store:
    return await InMemoryStore.gen()
