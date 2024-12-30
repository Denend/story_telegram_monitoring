from aiogram.types import Chat, Message, CallbackQuery, TelegramObject, InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from typing import Optional, Union

from services.logger import logger
from bot.telegram_bot import bot

class EventAttributes:
	"""Класс для атрибутов Telegram-сообщения/обработки"""
	async def __call__(self, event: TelegramObject, state: FSMContext) -> None:
		if isinstance(event, CallbackQuery):
			self.call = event
			self.message = event.message
		elif isinstance(event, Message):
			self.message = event
		else:
			raise ValueError("Event must be Message or CallbackQuery")

		self.user_id = event.from_user.id
		self.username = event.from_user.username
		self.first_name = event.from_user.first_name
		self.msg_text = self.message.text or self.message.caption
		self.html_text = self.message.html_text
		self.state = state

		self.ds = await state.get_data()

class SafeMessageHandler:
	"""Утилита для безопасного вызова методов Message, предотвращает исключения"""
	async def message_delete(self, message: Message, is_show_log: bool = True) -> Optional[bool]:
		try:
			return await message.delete()
		except Exception as e:
			if is_show_log:
				logger.warning("Ошибка при вызове `delete`: %s", e)

	async def message_edit_reply_markup(
		self,
		message: Message,
		reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]],
		is_show_log: bool = True
	) -> Optional[Message]:
		try:
			return await message.edit_reply_markup(reply_markup=reply_markup)
		except Exception as e:
			if is_show_log:
				logger.warning("Ошибка при вызове `edit_reply_markup`: %s", e)

	async def message_edit_text(self, message: Message, text: str, is_show_log: bool = True, **kwargs) -> Optional[Message]:
		try:
			return await message.edit_text(text=text, **kwargs)
		except Exception as e:
			if is_show_log:
				logger.warning("Ошибка при вызове `edit_text`: %s", e)

	async def message_reply(self, message: Message, text: str, **kwargs) -> Message:
		try:
			return await message.reply(text=text, **kwargs)
		except:
			return await message.answer(text=text, **kwargs)

	async def get_chat(self, chat_id: Union[int, str], is_show_log: bool = True) -> Optional[Chat]:
		try:
			return await bot.get_chat(chat_id)
		except Exception as e:
			if is_show_log:
				logger.warning("Ошибка при вызове `get_chat`: %s", e)
