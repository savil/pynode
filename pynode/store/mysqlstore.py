import asyncio
import json
from typing import Any, ClassVar, Dict, Optional

import aiomysql

from pynode.node import nodetype
from pynode.util.exceptions import SystemBadError
from pynode.store.store import NodeRow, node_row_from_dict

class MysqlStore:
    _singleton: ClassVar[Optional['MysqlStore']] = None
    _fetch_limit = 1000

    def __init__(self):
        pass

    @staticmethod
    async def gen() -> 'MysqlStore':
        if MysqlStore._singleton is None:
            MysqlStore._singleton = MysqlStore()
        return MysqlStore._singleton

    # TODOs savil. Convert to using pool? how does that work
    # with sharded mysql dbs? one pool per shard? seems excessive.
    #
    # pre-sharding, should set up one pool for lifetime of web-request
    # at least.
    async def _connect(self) -> aiomysql.Connection:
        return await aiomysql.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="pynodepass",
            db="pynode",
            loop=asyncio.get_running_loop()
        )

    async def create_node(self, node_type: nodetype.NodeType, data_dict: Dict[str, Any]) -> int:
        data_json = json.dumps(data_dict) # TODOs savil. sanitize this.
        sql_statement = f"INSERT INTO node (type, data) VALUES ({node_type.value}, '{data_json}')"
        return await self._execute_write_single(sql_statement)

    async def fetch_node_by_id(self, row_id: int) -> Optional[NodeRow]:
        sql_statement = f"SELECT * FROM node WHERE id={row_id}"
        row_dict = await self._execute_read_single(sql_statement)
        if row_dict is None:
            return None
        return node_row_from_dict(row_dict)

    # returns the id of the inserted row, if it succeeds
    # throws a SystemBadError if not
    async def _execute_write_single(self, sql: str) -> int:
        last_row_id = None
        conn = await self._connect()
        async with conn.cursor() as cur:
            num_rows_affected = await cur.execute(sql)
            if num_rows_affected is not None:
                last_row_id = cur.lastrowid

        await conn.commit()
        await conn.ensure_closed()

        if last_row_id is None:
            raise SystemBadError(f"failed to execute write sql-write: {sql}")

        return last_row_id

    async def _execute_read_single(self, sql: str) -> Optional[Dict[str, Any]]:
        result = None
        conn = await self._connect()
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sql)
            result = await cur.fetchone()

        conn.close()
        if result is None:
            return None

        return result
