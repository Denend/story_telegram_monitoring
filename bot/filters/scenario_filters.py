from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message, TelegramObject
from aiogram.fsm.context import FSMContext

class MediaCountFilter(Filter):
	def __init__(self, min_range: int, max_range: int) -> None:
		self.min_range = min_range
		self.max_range = max_range

	async def __call__(self, message: Message, state: FSMContext) -> bool:
		ds = await state.get_data()
		media_count = len(ds.get("media", []))
		return self.min_range <= media_count <= self.max_range

class MessageIDFilter(Filter):
	async def __call__(self, query: TelegramObject, state: FSMContext) -> bool:
		if isinstance(query, CallbackQuery):
			message = query.message
		ds = await state.get_data()
		msg_id = ds.get("msg_id")
		return message.message_id == msg_id

