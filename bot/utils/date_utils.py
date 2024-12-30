import pytz
from datetime import datetime

from config import TIMEZONE

def get_today(region: str = TIMEZONE) -> datetime:
	return datetime.now(pytz.timezone(region)).replace(tzinfo=None)

def get_date_as_string(date: datetime) -> str:
	return date.isoformat()

def get_date_from_string(date_str: str) -> datetime:
	return datetime.fromisoformat(date_str)
