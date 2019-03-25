from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
from typing import Any, Dict, Generic, Type, TypeVar

from pynode.node import nodetype
from pynode.store.store import NodeRow
from pynode.store import factory as store_factory

@dataclass(frozen=True)
class NodeDataTuple:
    id: int
    created: int
    type: nodetype.NodeType
    updated: int


def node_row_as_flattened_dict(row: NodeRow) -> Dict[str, Any]:
    data_dict = json.loads(row.data)
    row_dict = row._asdict()
    del row_dict['data']

    # combine row and data dicts
    return {**row_dict, **data_dict}

T = TypeVar('T', bound=NodeDataTuple)
class Node(Generic[T]):
    def __init__(self, data_constructor: Type[T], row: NodeRow) -> None:
        flattened_row = node_row_as_flattened_dict(row)
        self._data: T = data_constructor(**flattened_row)


class NodeMutator(ABC):

    def __init__(self, node_type: nodetype.NodeType) -> None:
        self._node_type = node_type

    async def create(self) -> int:
        data_dict = self.get_data_dict() # should this become a mutation object?
        node_type = self.get_node_type()
        #store_instance = await store_factory.inmemory()
        store_instance = await store_factory.mysql()
        return await store_instance.create_node(node_type, data_dict)

    @abstractmethod
    def get_data_dict(self) -> Dict[str, Any]:
        pass

    def get_node_type(self) -> nodetype.NodeType:
        return self._node_type
