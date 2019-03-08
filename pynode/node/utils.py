from pynode.util.exceptions import ProgrammerError
from pynode.node.core import Node, NodeDataTuple, NodeType
from pynode.node.user_node import UserNode, UserNodeData
from typing import Tuple, Type

def node_type_to_class(node_type: NodeType) -> Tuple[Type[Node], Type[NodeDataTuple]]:
    if node_type == NodeType.USER:
        return UserNode, UserNodeData
    else:
        raise ProgrammerError(f"unknown node type {node_type}")
