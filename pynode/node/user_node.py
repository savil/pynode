from dataclasses import dataclass
from typing import Any, Dict
from pynode.node.nodetype import NodeType

from pynode.node import core

@dataclass(frozen=True)
class UserNodeData(core.NodeDataTuple):
    name: str
    twitter_handle: str
    id: int
    created: int
    type: NodeType
    updated: int

class UserNode(core.Node[UserNodeData]):

    def get_name(self) -> str:
        return self._data.name

    def get_twitter_handle(self) -> str:
        return self._data.twitter_handle

class UserNodeMutator(core.NodeMutator):

    def __init__(self) -> None:
        self._name: str = ''
        self._twitter_handle: str = ''
        super().__init__(NodeType.USER)

    def set_name(self, name: str) -> 'UserNodeMutator':
        self._name = name
        return self

    def set_twitter_handle(self, twitter_handle: str) -> 'UserNodeMutator':
        self._twitter_handle = twitter_handle
        return self

    def get_data_dict(self) -> Dict[str, Any]:
        return {"name": self._name, "twitter_handle": self._twitter_handle}
