from redis.asyncio.client import Redis
from redis.asyncio.connection import ConnectionPool

from services.logger import logger
from .redis_config import REDIS_URL

pool = ConnectionPool.from_url(REDIS_URL)
redis = Redis(connection_pool=pool)
logger.info("Redis connected")
