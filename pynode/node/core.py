from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
from typing import Any, Dict, Generic, Type, TypeVar

from pynode.store import mysqlstore
from pynode.node import nodetype
from pynode.store import store

@dataclass(frozen=True)
class NodeDataTuple:
    id: int
    created: int
    type: nodetype.NodeType
    updated: int


def node_row_as_flattened_dict(row: store.NodeRow) -> Dict[str, Any]:
    data_dict = json.loads(row.data)
    row_dict = row._asdict()
    del row_dict['data']

    # combine row and data dicts
    return {**row_dict, **data_dict}

T = TypeVar('T', bound=NodeDataTuple)
class Node(Generic[T]):
    def __init__(self, data_constructor: Type[T], row: store.NodeRow) -> None:
        flattened_row = node_row_as_flattened_dict(row)
        self._data: T = data_constructor(**flattened_row)


class NodeMutator(ABC):

    def __init__(self, node_type: nodetype.NodeType) -> None:
        self._node_type = node_type

    async def create(self) -> int:
        data_dict = self.get_data_dict() # should this become a mutation object?
        node_type = self.get_node_type()
        store_instance = await mysqlstore.MysqlStore.gen()
        return await store_instance.create_node(node_type, data_dict)

    @abstractmethod
    def get_data_dict(self) -> Dict[str, Any]:
        pass

    def get_node_type(self) -> nodetype.NodeType:
        return self._node_type
