import uvicorn
from aiogram.types import Update
from fastapi import FastAPI

from services.logger import logger
from config import WEBHOOK_URL, WEBHOOK_PATH, APP_HOST, APP_PORT
from . import bot, dp

class Webhook:
	def __init__(self) -> None:
		self.app = FastAPI()

	async def __call__(self) -> None:
		"""Запуск FastAPI сервера с вебхуком."""
		await self.webhook_app()
		await self.webhook_run()

	async def webhook_app(self) -> None:
		"""Конфигурация вебхука через FastAPI."""
		@self.app.on_event("startup")
		async def on_startup():
			await bot.set_webhook(url=WEBHOOK_URL)
			logger.info("Bot started")

		@self.app.post(WEBHOOK_PATH)
		async def bot_webook(update: dict):
			"""Обработка обновлений через вебхук."""
			try:
				telegram_update = Update(**update)
				await dp.feed_update(bot=bot, update=telegram_update)
			except Exception as e:
				logger.exception(f'Error processing update: {e}')
			finally:
				return {'status': 'ok'}

		@self.app.on_event('shutdown')
		async def on_shutdown():
			"""Закрытие сессии при остановке приложения."""
			await bot.session.close()
			logger.info('Bot stoped')

		@self.app.get('/')
		async def root():
			"""Корневая страница приложения."""
			return {'Developer': 'https://t.me/matthew_0203'}

	async def webhook_run(self) -> None:
		config = uvicorn.Config(app=self.app, host=APP_HOST, port=APP_PORT, log_level='info')
		server = uvicorn.Server(config)
		await server.serve()

