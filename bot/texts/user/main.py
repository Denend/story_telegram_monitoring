from enum import Enum

from bot.utils.date_utils import get_today

class TextUser(Enum):
	REGISTRATION = "Welcome, {first_name}!\n"
	MAIN_MENU = (
		"Your ID: <code>{id}</code>\n"
		"Your username: <b>{username}</b>\n\n"
		"Validator Address: <code>{validator_address}</code>\n"
		"Consensus Address: <code>{consensus_address}</code>\n\n"
		"Uptime: <b>{last_uptime}</b>\n\n"
		"All time uptime: <b>{alltime_uptime}</b>\n\n"
		"Total missed blocks: <b>{total_missed_blocks}</b>\n\n"
		"The last update on the server: <b>{last_date}</b>"
	)

	UPDATE_UPTIME = (
		"❗️ <b>Your uptime dropped by {low_uptime_percent}%</b>\n\n"
		# "Период мониторинга аптайма с {start_date} до {last_date}\n\n"
		# "Первоначальный аптайм с момента мониторинга: {start_uptime}%\n"
		"🔹 Current uptime: {last_uptime}%"
	)

	MISSED_BLOCKS = (
		"🛑 <b>Blocks missed last time: {count_missed_blocks}</b>\n"
		"<i>"
		"- Missed blocks №: {missed_blocks}\n"
		"- Checked blocks: {start_height} - {end_height}\n"
		"- Total blocks missed: {total_missed_blocks}"
		# "- Number of checked blocks: {count_blocks}\n"
		"</i>\n\n"
		"ᴘᴏᴡᴇʀᴇᴅ ʙʏ ꜰᴛᴘ"
	)

	SWITCH_MONITORING = "Monitoring for «{name}» is {on_off}"
	UNTIE_ADDRESS = "The address has been successfully unlinked!\nEnter <b>/start</b> to add a new address"

	def format_text(self, **kwargs) -> str:
		try:
			if "last_uptime" not in kwargs:
				kwargs["alltime_uptime"] = "The data will be updated within 5 minutes"
				kwargs["last_uptime"] = "The data will be updated within 5 minutes"
				kwargs["last_date"] = "The data will be updated within 5 minutes"
			if "total_missed_blocks" not in kwargs:
				kwargs["total_missed_blocks"] = "The data will be updated within 5 minutes"
			if kwargs.get("username"): kwargs["username"] = "@"+kwargs["username"]
			return self.value.format(**kwargs)
		except KeyError as e:
			raise ValueError(f"Missing key for formatting: {e}") from None

class TextUserWarning(Enum):
	UPDATE_POST = "Current data is up-to-date!"

	def format_text(self, **kwargs) -> str:
		try:
			return self.value.format(**kwargs)
		except KeyError as e:
			raise ValueError(f"Missing key for formatting: {e}") from None
