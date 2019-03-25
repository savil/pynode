from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, NamedTuple, Optional

from pynode.node import nodetype

NodeRow = NamedTuple(
    'NodeRow',
    [('id', int),
     ('type', int),
     ('data', str),
     ('updated', int),
     ('created', int),
    ]
)

def node_row_from_dict(raw: Dict[str, Any]) -> NodeRow:
    return NodeRow(
        id=raw['id'],
        type=raw['type'],
        data=raw['data'],
        updated=raw['updated'],
        created=raw['created']
    )

class StoreType(Enum):
    MYSQL = 1
    IN_MEMORY = 2

class Store(ABC):

    def __init__(self):
        pass

    @abstractmethod
    async def create_node(self, node_type: nodetype.NodeType, data_dict: Dict[str, Any]) -> int:
        ...

    @abstractmethod
    async def fetch_node_by_id(self, row_id: int) -> Optional[NodeRow]:
        ...
