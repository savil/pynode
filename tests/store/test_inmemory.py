import json
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
        store_instance = await self._create_store()
        data = {"name": "savil"}
        node_id = await store_instance.create_node(NodeType.USER, data)
        assert node_id == 1
        node_row = await store_instance.fetch_node_by_id(node_id)
        assert node_row is not None
        assert node_row.id == 1
        assert node_row.data == json.dumps(data)
