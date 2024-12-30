import logging
from logging import getLogger, StreamHandler, Formatter, DEBUG, INFO, WARNING

from config import LOGGER_NAME

logger = getLogger(LOGGER_NAME)
logger.setLevel(INFO)

# aiogram_logger = getLogger("aiogram")
# aiogram_logger.setLevel(DEBUG)

handler = StreamHandler()

formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # формат
handler.setFormatter(formatter)

logger.addHandler(handler)
# aiogram_logger.addHandler(handler)


getLogger("apscheduler").setLevel(WARNING)
getLogger("uvicorn").disabled = True
getLogger("uvicorn.access").disabled = True
getLogger("uvicorn.error").disabled = True
