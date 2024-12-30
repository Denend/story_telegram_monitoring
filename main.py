import asyncio

from initializer import Initializer
from services.logger import logger

async def main():
	initializer = Initializer()
	await initializer()

if __name__ == '__main__':
	asyncio.run(main())