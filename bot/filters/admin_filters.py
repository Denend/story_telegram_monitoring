from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message, TelegramObject
from aiogram.fsm.context import FSMContext

from services.db import SimpleQueries

class IsAdminFilter(Filter):
	async def __call__(self, message: Message, state: FSMContext) -> None:
		is_admin = await SimpleQueries.get_val_data(table="users", id=message.from_user.id, columns="is_admin")
		return is_admin
