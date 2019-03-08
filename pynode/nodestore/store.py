import aiomysql, asyncio, json
import pynode.node.core as node

from pynode.node.core import NodeRow
from pynode.node.nodetype import NodeType
from typing import Any, ClassVar, Dict, Optional

class Store:
    _singleton: ClassVar[Optional[Store]] = None
    _fetch_limit = 1000

    def __init__(self):
        # TODO savil. prevent this from being directly called

        self._pool = aiomysql.create_pool(
            host = "127.0.0.1",
            port = 3306,
            user = "root",
            password = "pynodepass",
            db = "mysql",
            loop = asyncio.get_running_loop()
        )

    @staticmethod
    def get() -> Store:
        if Store._singleton is None:
            Store._singleton = Store()
        return Store._singleton


    async def create_node(self, node_type: NodeType, data_dict: Dict[str, Any]) -> int:
        data_json = json.dumps(data_dict)
        sql_statement = f"INSERT INTO node (type, data) VALUES ({node_type}, {data_json})"
        return await self._execute_write_single(sql_statement)

    async def fetch_node_by_id(self, row_id: int) -> Optional[NodeRow]:
        sql_statement = f"SELECT * FROM node WHERE id={row_id}"
        row_dict = await self._execute_read_single(sql_statement)
        if row_dict is None:
            return None;
        return node.node_row_from_dict(row_dict)

    # returns the id of the inserted row, if it succeeds
    # throws a SystemError if not
    async def _execute_write_single(self, sql: str) -> int:
        last_row_id = None
        async with self._pool.acquire() as conn:
            async with conn.cursor() as cur:
                num_rows_affected = await cur.execute(sql)
                if num_rows_affected != None:
                    last_row_id = cur.lastrowid
        self._pool.close()
        await self._pool.wait_closed()

        if last_row_id is None:
            raise SystemError(f"failed to execute write sql-write: {sql}")

        return last_row_id

    async def _execute_read_single(self, sql: str) -> Optional[Dict[str, Any]]:
        result = None
        async with self._pool.acquire() as conn:
            async with conn.cursor(conn.DictCursor) as cur:
                await cur.execute(sql)
                result = await cur.fetchmany(Store._fetch_limit)

        self._pool.close()
        await self._pool.wait_closed()

        return result
