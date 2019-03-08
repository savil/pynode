from dataclasses import dataclass
from typing import Any, Dict, NamedTuple, Generic, TypeVar
from pynode.node.nodetype import NodeType

from pynode.node.core import Node, NodeDataTuple, NodeMutator, NodeRow

@dataclass
class UserNodeData(NodeDataTuple):
    name: str
    twitter_handle: str
    id: int
    created: int
    type: NodeType
    updated: int

class UserNode(Node[UserNodeData]):

    def get_name(self) -> str:
        return self._data.name

    def get_twitter_handle(self) -> str:
        return self._data.twitter_handle

class UserNodeMutator(NodeMutator[UserNode]):

    def __init__(self) -> None:
        super().__init__(NodeType.USER)

    def set_name(self, name: str) -> UserNodeMutator:
        self._name = name
        return self

    def set_twitter_handle(self, twitter_handle: str) -> UserNodeMutator:
        self._twitter_handle = twitter_handle
        return self

    def get_data_dict(self) -> Dict[str, Any]:
        return {"name": self._name, "twitter_handle": self._twitter_handle}
