import json

from ..date_utils import get_date_from_string
from services.redis import redis
from services.redis.redis_config import UPTIME_DATA_KEY, ALLTIME_UPTIME_DATA_KEY, TOTAL_MISSED_BLOCKS_KEY

async def get_data_from_redis(user_id: int) -> dict:
	uptime_data_key = f"{UPTIME_DATA_KEY}:{user_id}"
	alltime_uptime_data_key = f"{ALLTIME_UPTIME_DATA_KEY}:{user_id}"
	total_missed_blocks_key = f"{TOTAL_MISSED_BLOCKS_KEY}:{user_id}"

	data_dict = {}

	data = await redis.get(uptime_data_key)
	if data:
		json_data = json.loads(data)

		data_dict["last_uptime"] = f"{json_data['last_uptime']}%"
		data_dict["last_date"] = get_date_from_string(json_data["last_date"])

	data = await redis.get(alltime_uptime_data_key)
	if data:
		data_dict["alltime_uptime"] = f"{round(float(data.decode('utf-8')), 2)}%"

	data = await redis.get(total_missed_blocks_key)
	if data:
		data_dict["total_missed_blocks"] = data.decode("utf-8")

	return data_dict


