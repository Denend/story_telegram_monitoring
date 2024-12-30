from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Dict, List, Optional

class AdminCallbackData(CallbackData, prefix="admin"):
	action: str

class AdminConfirmCallbackData(CallbackData, prefix="admin"):
	action: str
	target: str

class SponsorCallbackData(CallbackData, prefix="admin"):
	action: str
	id: int

class AdminInlineMarkup:
	@staticmethod
	def test(target: str):
		builder = InlineKeyboardBuilder()



		builder.adjust(1)
		return builder.as_markup()

