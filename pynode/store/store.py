from typing import Any, Dict, NamedTuple

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
