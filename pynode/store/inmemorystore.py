import json
from time import time
from typing import Any, ClassVar, Dict, Optional

from pynode.node import nodetype
from pynode.store.store import NodeRow, node_row_from_dict, Store

class InMemoryStore(Store):
    _singleton: ClassVar[Optional['InMemoryStore']] = None
    _last_node_id: int = 0
    # NodeTable is Dict(id => NodeRow)
    _node_table: Dict[int, NodeRow] = {}
    # EdgeTable is Dict(from_id => Dict(type => EdgeRow))

    @staticmethod
    async def gen() -> 'InMemoryStore':
        if InMemoryStore._singleton is None:
            InMemoryStore._singleton = InMemoryStore()
        return InMemoryStore._singleton

    async def create_node(self, node_type: nodetype.NodeType, data_dict: Dict[str, Any]) -> int:
        node_id = self._make_node_id()

        data_json = json.dumps(data_dict) # TODOs savil. sanitize this.
        row_dict = _make_row_dict(node_id, node_type, data_json)
        node_row = node_row_from_dict(row_dict)

        self._node_table[node_id] = node_row
        return node_id

    async def fetch_node_by_id(self, row_id: int) -> Optional[NodeRow]:
        if row_id in self._node_table:
            return self._node_table[row_id]

        return None

    def _make_node_id(self):
        self._last_node_id = self._last_node_id + 1
        return self._last_node_id

    @classmethod
    def clear_singleton(cls):
        cls._singleton = None

# Helper Functions:

def _make_row_dict(node_id: int, node_type, data_json: str) -> Dict[str, Any]:
    utctime_now = int(time())
    return {
        'id': node_id,
        'type': node_type,
        'data': data_json,
        'updated': utctime_now,
        'created': utctime_now
    }
