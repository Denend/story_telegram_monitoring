from config import TIMEZONE
from .db_manager import db

class DatabaseInit:
	async def __call__(self) -> None:
		await self._set_default_timezone()
		await self._create_tables()

	async def _set_default_timezone(self) -> None:
		await db.execute(f"SET TIME ZONE '{TIMEZONE}'")

	async def _create_tables(self) -> None:
		CREATE_USERS_TABLE = """
			CREATE TABLE IF NOT EXISTS users (
				id							BIGINT		PRIMARY KEY,
				first_name					TEXT,
				username					TEXT,
				validator_address			TEXT,
				consensus_address			TEXT,
				is_uptime_monitoring		BOOL		DEFAULT TRUE,
				is_miss_blocks_monitoring	BOOL		DEFAULT TRUE,
				start_date					TIMESTAMP	DEFAULT now(),
				last_activity				TIMESTAMP	DEFAULT now()
			)"""

		await db.execute(CREATE_USERS_TABLE)

db_init = DatabaseInit()
