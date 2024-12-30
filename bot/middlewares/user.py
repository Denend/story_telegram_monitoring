from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject
from typing import Any, Awaitable, Callable, Dict

from services.db import db

class UserMiddleware(BaseMiddleware):
	def __init__(self) -> None:
		super().__init__()

	async def __call__(self,
					handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
					event: TelegramObject,
					data: Dict[str, Any]
					) -> Any:
		if (
			isinstance(event, Message) and
			event.text and
			event.entities and
			event.entities[0].type == 'bot_command' and
			event.text.split()[0] in ('/start')
			):
			return await handler(event, data)

		user_id = event.from_user.id
		username = event.from_user.username
		first_name = event.from_user.first_name

		if await db.fetchval("SELECT id FROM users WHERE id = $1", user_id):
			await db.execute("UPDATE users SET first_name = $1, username = $2, last_activity = now() WHERE id = $3", first_name, username, user_id)
			return await handler(event, data)

		await event.answer(text="You are not registered in the bot!\nEnter /start to use the bot.")
