from dataclasses import dataclass
from pynode.node.nodetype import NodeType
from pynode.nodestore.store import Store
from typing import Any, Dict, Generic, NamedTuple, Type, TypeVar

import pynode.node.utils as utils
import json

NodeRow = NamedTuple(
    'NodeRow',
    [('id', int),
     ('type', int),
     ('data', str),
     ('updated', int),
     ('created', int),
    ]
)

def node_row_from_dict(d: Dict[str, Any]) -> NodeRow:
    return NodeRow(id=d['id'], type=d['type'], data=d['data'], updated=d['updated'], created=d['created'])

@dataclass(frozen=True)
class NodeDataTuple:
    id: int
    created: int
    type: NodeType
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

    @staticmethod
    def create(node_row: NodeRow) -> Node:
        node_type = NodeType(node_row.type)
        node_cls, node_data_cls = utils.node_type_to_class(node_type)
        return node_cls(node_data_cls, node_row)

class NodeLoader:
    @staticmethod
    async def load(node_id: int) -> Node:
        node_row = await Store.get().fetch_node_by_id(node_id)
        if node_row is None:
            raise SystemError(f"unable to find newly created node, from id: {node_id}")

        return Node.create(node_row)

TM = TypeVar('TM', bound=Node)
class NodeMutator(Generic[TM]):

    def __init__(self, node_type: NodeType) -> None:
        self._node_type = node_type

    async def create(self) -> TM:
        data_dict = self.get_data_dict() # should this become a mutation object?
        node_type = self.get_node_type()
        node_id = await Store.get().create_node(node_type, data_dict)

        # we know the type is the right kind of Node
        return await NodeLoader.load(node_id) # type: ignore

    def get_data_dict(self) -> Dict[str, Any]:
        ...

    def get_node_type(self) -> NodeType:
        return self._node_type
