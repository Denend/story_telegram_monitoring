from bot.telegram_bot.bot_runner import BotRunner
from bot.utils.uptime.update_uptime import UpdateUptime
from bot.utils.uptime.uptime_blocks import UptimeBlocks
from services.db import db, db_init

class Initializer:
	def __init__(self) -> None:
		self.update_uptime = UpdateUptime()
		self.uptime_blocks = UptimeBlocks()
		self.bot_runner = BotRunner()

	async def __call__(self) -> None:
		await db.connect()
		await db_init()
		await self.update_uptime()
		await self.uptime_blocks()
		await self.bot_runner()

