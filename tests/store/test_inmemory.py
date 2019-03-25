import pytest
from pynode.store import factory as store_factory
from pynode.store.inmemorystore import InMemoryStore
from pynode.node.nodetype import NodeType

class TestInMemoryStore():

    async def _create_store(self):
        InMemoryStore.clear_singleton()
        return await store_factory.inmemory()

    @pytest.mark.asyncio
    async def test_create_node(self):
        store_instance = await self._create_store()
        node_id = await store_instance.create_node(NodeType.USER, {})
        assert node_id == 1

    @pytest.mark.asyncio
    async def test_create_multiple_nodes(self):
        store_instance = await self._create_store()
        await store_instance.create_node(NodeType.USER, {})
        node_id = await store_instance.create_node(NodeType.USER, {})
        assert node_id == 2

    @pytest.mark.asyncio
    async def test_fetch_node_by_id(self):
        pass
