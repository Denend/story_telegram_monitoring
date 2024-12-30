from aiogram import Router

from . import dp
from .webhook import Webhook

from bot.handlers import user
from bot.handlers.user import add_address
from bot.handlers.user import main

from bot.middlewares.throttling import ThrottlingMiddleware
from bot.middlewares.album import AlbumMiddleware
from bot.middlewares.user import UserMiddleware

class BotRunner:
	def __init__(self) -> None:
		self.router = Router()

	async def __call__(self) -> None:
		"""Initializing and launching the bot"""
		await self.register_middlewares()
		await self.register_handlers()
		await self.webhook_run()

	async def register_middlewares(self) -> None:
		"""Registration of the middleware"""
		dp.message.middleware.register(UserMiddleware())
		dp.message.middleware.register(AlbumMiddleware())
		dp.message.middleware.register(ThrottlingMiddleware())

		dp.callback_query.middleware.register(UserMiddleware())
		dp.callback_query.middleware.register(ThrottlingMiddleware())

	async def register_handlers(self) -> None:
		"""Registration of handlers"""

		# Commands
		user.CommandHandlers(self.router)

		# Messages
		add_address.MessageHandlers(self.router)

		# Callbacks
		main.CallbackHandlers(self.router)


		dp.include_router(self.router)

	async def webhook_run(self) -> None:
		self.webhook = Webhook()
		await self.webhook()