from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Dict, List, Optional

class UserCallbackData(CallbackData, prefix="user"):
	action: str

class UserSwitchCallbackData(UserCallbackData, prefix="user"):
	column: str

class UserInlineMarkup:
	@staticmethod
	def main_menu(is_uptime_monitoring: bool, is_miss_blocks_monitoring: bool):
		builder = InlineKeyboardBuilder()
		builder.button(text="🔄 Update", callback_data=UserCallbackData(action="update_post"))
		builder.button(
			text=f"{'✅' if is_uptime_monitoring else '❌'} Uptime Monitoring",
			callback_data=UserSwitchCallbackData(action="switch", column="is_uptime_monitoring")
			)
		builder.button(
			text=f"{'✅' if is_miss_blocks_monitoring else '❌'} Miss Blocks Monitoring",
			callback_data=UserSwitchCallbackData(action="switch", column="is_miss_blocks_monitoring"))
		builder.button(text="⛓️‍💥 Change Validator Address", callback_data=UserCallbackData(action="untie_address"))
		builder.adjust(1, 2)
		return builder.as_markup()
