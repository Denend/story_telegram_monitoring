import asyncio
import asyncpg
from asyncpg import Connection, Record
from functools import wraps
from typing import List, Optional, Any

from services.logger import logger
from .db_config import CONNECTION_ARGS

def with_connection(func):
	@wraps(func)
	async def wrapper(self, *args, **kwargs):
		async with self.pool.acquire() as conn:
			return await func(self, conn, *args, **kwargs)

	return wrapper

class DatabaseManager:
	async def connect(self) -> None:
		self.pool = await asyncpg.create_pool(**CONNECTION_ARGS)
		logger.info("Postgresql connected")

	async def close(self) -> None:
		if self.pool:
			await self.pool.close()

	@with_connection
	async def fetch(self, conn: Connection, query: str, *args: Any) -> List[Record]:
		result = await conn.fetch(query, *args)
		return result

	@with_connection
	async def fetchrow(self, conn: Connection, query: str, *args: Any) -> Optional[Record]:
		result = await conn.fetchrow(query, *args)
		return result

	@with_connection
	async def fetchval(self, conn: Connection, query: str, *args: Any, column: int = 0) -> Any:
		result = await conn.fetchval(query, *args, column=column)
		return result

	@with_connection
	async def execute(self, conn: Connection, query: str, *args: Any) -> None:
		await conn.execute(query, *args)

	@with_connection
	async def executemany(self, conn: Connection, query: str, values: List[tuple]) -> None:
		await conn.executemany(query, values)

db = DatabaseManager()
