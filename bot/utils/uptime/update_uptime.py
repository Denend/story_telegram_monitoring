import asyncio
import json
from asyncpg import Record
from aiohttp import ClientSession
from typing import Union

from ..date_utils import get_today, get_date_as_string, get_date_from_string
from services.api.story.ts import TSClient
from services.api.story.asttp import ASTTPClient
from services.db import db
from services.redis import redis
from services.redis.redis_config import UPTIME_DATA_KEY
from bot.telegram_bot import bot
from bot.texts.user import TextUser

ts_client = TSClient()
asttp_client = ASTTPClient()

class UpdateUptime:
	def __init__(self) -> None:
		self.cycle = True

	async def __call__(self):
		asyncio.create_task(self.start())

	async def start(self) -> None:
		count_cycle = 0
		while self.cycle:
			count_cycle += 1
			await ts_client.connect()
			await asttp_client.connect()

			users = await db.fetch("SELECT id, validator_address, consensus_address, is_uptime_monitoring FROM users WHERE validator_address IS NOT NULL")

			tasks = [
				asyncio.create_task(self.update_uptime(user=user, ts_client=ts_client, asttp_client=asttp_client))
				for user in users
			]

			await asyncio.gather(*tasks)

			print("cycle update_uptime:", count_cycle)

			await asyncio.sleep(60)


	async def insert_redis_data(self, uptime_data_key: str, success_blocks_percent: Union[float, int], date_str: str) -> None:
		uptime_data = json.dumps({
			"start_uptime": success_blocks_percent,
			"last_uptime": success_blocks_percent,
			"start_date": date_str,
			"last_date": date_str
			})
		await redis.set(uptime_data_key, value=uptime_data, ex=172800)

	async def update_redis_data(self, uptime_data_key: str, **kwargs) -> None:
		uptime_data = json.dumps({**kwargs})
		await redis.set(uptime_data_key, value=uptime_data, ex=172800)

	async def get_success_blocks_percent(self, user: Record, ts_client: ClientSession, asttp_client: ClientSession) -> Union[float, int]:
		uptime = await ts_client.get_uptime(address=user["validator_address"])
		slashing_signing_infos = await asttp_client.get_slashing_signing_infos(address=user["consensus_address"])

		if uptime and not slashing_signing_infos.get("error"):
			window_start = uptime["windowUptime"]["windowStart"]
			window_end = uptime["windowUptime"]["windowEnd"]
			missed_blocks_counter = int(slashing_signing_infos["val_signing_info"].get("missed_blocks_counter", 0))

			count_blocks = window_end - window_start
			missed_blocks_percent = missed_blocks_counter / count_blocks * 100
			success_blocks_percent = round(100 - missed_blocks_percent, 2)

			return success_blocks_percent

	async def update_uptime(self, user: Record, ts_client: ClientSession, asttp_client: ClientSession) -> None:
		uptime_data_key = f"{UPTIME_DATA_KEY}:{user['id']}"

		today = get_today().replace(microsecond=0)
		date_str = get_date_as_string(date=today)

		success_blocks_percent = await self.get_success_blocks_percent(user=user, ts_client=ts_client, asttp_client=asttp_client)

		if not success_blocks_percent:
			return

		bytes_uptime_data = await redis.get(uptime_data_key)
		if bytes_uptime_data:
			uptime_data = json.loads(bytes_uptime_data)

			uptime_data["last_uptime"] = success_blocks_percent
			uptime_data["last_date"] = date_str

			if success_blocks_percent < uptime_data["start_uptime"]:
				low_uptime_percent = round(uptime_data["start_uptime"] - uptime_data["last_uptime"], 2)
				if low_uptime_percent >= 0.05:
					await self.insert_redis_data(uptime_data_key=uptime_data_key, success_blocks_percent=success_blocks_percent, date_str=date_str)
					return await self.uptime_low_handler(user=user, uptime_data=uptime_data, low_uptime_percent=low_uptime_percent)

			elif success_blocks_percent > uptime_data["start_uptime"]:
				# uptime_data["high_uptime"] = success_blocks_percent
				return await self.insert_redis_data(uptime_data_key=uptime_data_key, success_blocks_percent=success_blocks_percent, date_str=date_str)

			await self.update_redis_data(uptime_data_key=uptime_data_key, **uptime_data)

		else:
			await self.insert_redis_data(uptime_data_key=uptime_data_key, success_blocks_percent=success_blocks_percent, date_str=date_str)

	async def uptime_low_handler(self, user: Record, uptime_data: dict, low_uptime_percent: Union[float, int]) -> None:
		if user["is_uptime_monitoring"]:
			uptime_data["start_date"] = get_date_from_string(uptime_data["start_date"])
			uptime_data["last_date"] = get_date_from_string(uptime_data["last_date"])
			try:
				await bot.send_message(chat_id=user["id"], text=TextUser.UPDATE_UPTIME.format_text(low_uptime_percent=low_uptime_percent, **uptime_data))
			except Exception as e:
				pass
