import aiohttp

from .config import url_slashing_signing_infos

class ASTTPClient:
	def __init__(self):
		self.session = None

	async def connect(self):
		await self.close()
		self.session = aiohttp.ClientSession()

	async def close(self):
		if self.session:
			await self.session.close()
			self.session = None

	async def get_slashing_signing_infos(self, address: str, retry: int = 3) -> dict:
		while retry:
			try:
				async with self.session.get(f"{url_slashing_signing_infos}{address}") as response:
					data = await response.json()
					if data.get("code", 0) == 500:
						return {"error": "code 500"}
					return data
			except Exception as e:
				print("Error in TSClient `get_slashing_signing_infos`:", e)
				retry -= 1
				await asyncio.sleep(1)
		return {"error": "limit retry"}


