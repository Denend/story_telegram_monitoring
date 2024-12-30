import asyncio
import json
from asyncpg import Record
from aiohttp import ClientSession
from typing import Dict, List, Union

from ..date_utils import get_today, get_date_as_string, get_date_from_string
from services.api.story.ts import TSClient
from services.db import db
from services.redis import redis
from services.redis.redis_config import LAST_BLOCK_KEY, ALLTIME_UPTIME_DATA_KEY, TOTAL_MISSED_BLOCKS_KEY
from bot.telegram_bot import bot
from bot.texts.user import TextUser

ts_client = TSClient()

class UptimeBlocks:
	def __init__(self) -> None:
		self.cycle = True

	async def __call__(self):
		asyncio.create_task(self.start())

	async def start(self) -> None:
		count_cycle = 0
		while self.cycle:
			count_cycle += 1
			await ts_client.connect()

			users = await db.fetch(
				"""
				SELECT id, validator_address, consensus_address
				FROM users
				WHERE validator_address IS NOT NULL AND is_miss_blocks_monitoring IS TRUE
				"""
				)

			tasks = [
				asyncio.create_task(self.uptime_blocks(user=user, ts_client=ts_client))
				for user in users
			]

			await asyncio.gather(*tasks)

			print("cycle uptime_blocks:", count_cycle)

			await asyncio.sleep(30)

	def _get_total_missed_blocks(self, data: dict) -> None:
		historical_uptime = data["historicalUptime"]

		earliestHeight = historical_uptime["earliestHeight"]
		lastSyncHeight = historical_uptime["lastSyncHeight"]
		successBlocks = historical_uptime["successBlocks"]

		totalBlocks = lastSyncHeight - earliestHeight
		total_missed_blocks_percent = (successBlocks / (lastSyncHeight - earliestHeight)) * 100

		return totalBlocks - successBlocks, total_missed_blocks_percent

	async def uptime_blocks(self, user: Record, ts_client: ClientSession) -> None:
		last_block_key = f"{LAST_BLOCK_KEY}:{user['id']}"
		alltime_uptime_data_key = f"{ALLTIME_UPTIME_DATA_KEY}:{user['id']}"
		total_missed_blocks_key = f"{TOTAL_MISSED_BLOCKS_KEY}:{user['id']}"

		blocks = await ts_client.get_blocks_uptime(address=user["validator_address"])
		uptime_data = await ts_client.get_uptime(address=user["validator_address"])
		if not blocks or not uptime_data:
			return

		for entry in blocks:
			entry["height"] = int(entry["height"])

		sorted_blocks = sorted(blocks, key=lambda x: x["height"], reverse=True)[1:]

		bytes_last_block = await redis.get(last_block_key)

		height_block = sorted_blocks[0]["height"]

		total_missed_blocks, alltime_uptime = self._get_total_missed_blocks(data=uptime_data)

		await redis.set(last_block_key, value=height_block, ex=172800)
		await redis.set(alltime_uptime_data_key, value=alltime_uptime, ex=172800)
		await redis.set(total_missed_blocks_key, value=total_missed_blocks, ex=172800)

		missed_blocks = []

		if bytes_last_block:
			last_block = int(bytes_last_block)
			for block in sorted_blocks:
				if block["height"] <= last_block:
					return await self.sending_handler(
						user=user,
						missed_blocks=missed_blocks,
						last_block=last_block,
						height_block=height_block,
						blocks=sorted_blocks,
						total_missed_blocks=total_missed_blocks
						)
				if not block["signed"]:
					missed_blocks.append(block["height"])
			await self.sending_handler(
				user=user,
				missed_blocks=missed_blocks,
				last_block=last_block,
				height_block=height_block,
				blocks=sorted_blocks,
				total_missed_blocks=total_missed_blocks
				)


	async def sending_handler(
		self,
		user: Record,
		missed_blocks: List[int],
		last_block: int,
		height_block: int,
		blocks: List[Dict],
		total_missed_blocks: int
	) -> None:
		if missed_blocks:
			count_blocks = height_block - last_block
			if count_blocks > len(blocks):
				last_block = height_block - len(blocks)
				count_blocks = len(blocks)
			try:
				await bot.send_message(
					chat_id=user["id"],
					text=TextUser.MISSED_BLOCKS.format_text(
						start_height=last_block+1,
						end_height=height_block,
						count_blocks=count_blocks,
						count_missed_blocks=len(missed_blocks),
						missed_blocks=", ".join(map(str, missed_blocks)),
						total_missed_blocks=total_missed_blocks
						)
					)
			except Exception as e:
				pass
