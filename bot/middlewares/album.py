import asyncio
from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Any, Awaitable, Callable, Dict

class AlbumMiddleware(BaseMiddleware):
	album_data = {}

	def __init__(self, latency: float = 0.2):
		self.tasks = {}
		self.latency = latency

	async def __call__(self,
					handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
					event: Message,
					data: Dict[str, Any]
					) -> Any:
		if isinstance(event, Message) and event.media_group_id:
			await self.on_process_message(event, handler, data)
			return
		return await handler(event, data)

	async def process_album(self, media_group_id: str, handler, message: Message, data: dict):
		album = self.album_data.pop(media_group_id, [])

		data["album"] = album
		event = message.copy(update={"album": album})
		await handler(event, data)

		self.tasks.pop(media_group_id, None)

	async def schedule_album_processing(self, media_group_id: str, handler, message: Message, data: dict):
		if media_group_id in self.tasks:
			self.tasks[media_group_id].cancel()
		self.tasks[media_group_id] = asyncio.create_task(self._delayed_process_album(media_group_id, handler, message, data))

	async def _delayed_process_album(self, media_group_id, handler, message, data):
		try:
			await asyncio.sleep(self.latency)
			await self.process_album(media_group_id, handler, message, data)
		except asyncio.CancelledError:
			pass


	async def on_process_message(self, message: Message, handler, data: dict):
		group_id = message.media_group_id
		if group_id not in self.album_data:
			self.album_data[group_id] = []

		self.album_data[group_id].append(message)

		await self.schedule_album_processing(group_id, handler, message, data)

