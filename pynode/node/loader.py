from typing import Tuple, Type

from pynode.util.exceptions import ProgrammerError
from pynode.node import core
from pynode.node import user_node
from pynode.node.nodetype import NodeType
from pynode.nodestore import store

def node_type_to_class(node_type: NodeType) -> Tuple[Type[core.Node], Type[core.NodeDataTuple]]:

    if node_type == NodeType.USER:
        return user_node.UserNode, user_node.UserNodeData

    raise ProgrammerError(f"unknown node type {node_type}")


class NodeLoader:
    @staticmethod
    async def load(node_id: int) -> core.Node:
        store_instance = await store.Store.gen()
        node_row = await store_instance.fetch_node_by_id(node_id)
        if node_row is None:
            raise SystemError(f"unable to find newly created node, from id: {node_id}")

        node_type = NodeType(node_row.type)
        node_cls, node_data_cls = node_type_to_class(node_type)
        return node_cls(node_data_cls, node_row)
