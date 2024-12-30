import aiohttp
import asyncio
from typing import List

from .config import url_validators, url_blocks_uptime, url_accounts_address

class TSClient:
	def __init__(self):
		self.session = None

	async def connect(self):
		await self.close()
		self.session = aiohttp.ClientSession()

	async def close(self):
		if self.session:
			await self.session.close()
			self.session = None

	async def get_addresses_data(self, address: str) -> dict:
		try:
			async with self.session.get(url_accounts_address.format(address=address)) as response:
				items = await response.json()
				data = items["items"][0]["validator"]
				return {"operatorAddress": data["operatorAddress"], "consensusAddress": data["consensusAddress"]}
		except Exception as e:
			print("Error in TSClient `get_validator_address_data`:", e)
			return {"error": "Error"}

	async def get_validator_address_data(self, address: str, retry: int = 3) -> dict:
		while retry:
			try:
				async with self.session.get(f"{url_validators}{address}") as response:
					return await response.json()
			except Exception as e:
				print("Error in TSClient `get_validator_address_data`:", e)
				retry -= 1
				await asyncio.sleep(1)
		return {"error": "limit retry"}

	async def get_consensus_address(self, address: str) -> dict:
		data = await self.get_validator_address_data(address=address)
		if data:
			return data.get("consensusAddress")

	async def get_uptime(self, address: str) -> dict:
		data = await self.get_validator_address_data(address=address)
		if data:
			return data.get("uptime")

	async def get_blocks_uptime(self, address: str, retry: int = 3) -> List[dict]:
		while retry:
			try:
				async with self.session.get(f"{url_blocks_uptime}{address}") as response:
					return await response.json()
			except Exception as e:
				print("Error in TSClient `get_blocks_uptime`:", e)
				retry -= 1
				await asyncio.sleep(1)

# {
# 	'delegation': {
# 		'delegator_address': 'story15xdpesljm34mgllad7wgjfyknxmz8h9yw0kv30',
# 		'validator_address': 'storyvaloper15xdpesljm34mgllad7wgjfyknxmz8h9yqqzd6y',
# 		'shares': '1024000000000.000000000000000000',
# 		'rewards_shares': '1024000000000.000000000000000000'
# 	},
# 	'balance': {
# 		'denom': 'stake',
# 		'amount': '1024000000000'
# 	},
# 	'validator': {
# 		'operator_address': 'storyvaloper15xdpesljm34mgllad7wgjfyknxmz8h9yqqzd6y',
# 		'consensus_pubkey': {
# 			'type': 'tendermint/PubKeySecp256k1',
# 			'value': 'A40CKSnPaqYh4W/Yykl2rXMrn8Q3MfgrhmyJr7EnEOBo'
# 		},
# 		'status': 3,
# 		'tokens': 141024000000000,
# 		'delegator_shares': '141024000000000.000000000000000000',
# 		'unbonding_time': '1970-01-01T00:00:00Z',
# 		'commission': {
# 			'commission_rates': {
# 				'rate': '0.100000000000000000',
# 				'max_rate': '0.500000000000000000',
# 				'max_change_rate': '0.100000000000000000'
# 			},
# 			'update_time': '2024-12-02T05:48:27.872089353Z'
# 		},
# 		'min_self_delegation': '1024000000000',
# 		'support_token_type': 1,
# 		'rewards_tokens': '141024000000000.000000000000000000',
# 		'delegator_rewards_shares': '141024000000000.000000000000000000',
# 		'operatorAddress': 'storyvaloper15xdpesljm34mgllad7wgjfyknxmz8h9yqqzd6y',
# 		'hexAddress': 'A19A1CC3F2DC6BB47FFD6F9C89249699B623DCA4',
# 		'consensusAddress': 'storyvalcons15xdpesljm34mgllad7wgjfyknxmz8h9y5n33k9',
# 		'accountAddress': 'story15xdpesljm34mgllad7wgjfyknxmz8h9yw0kv30',
# 		'description': {
# 			'moniker': 'ftp_validator',
# 			'avatar': None,
# 			'socials': {
# 				'githubUrl': None,
# 				'twitterUrl': None,
# 				'webUrl': None
# 			}
# 		},
# 		'participation': {
# 			'rate': 0,
# 			'total': 0,
# 			'voted': 0
# 		},
# 		'signingInfo': {
# 			'bondedHeight': 0,
# 			'jailedUntil': '',
# 			'tombstoned': False
# 		},
# 		'uptime': {
# 			'historicalUptime': {
# 				'earliestHeight': 1061899,
# 				'lastSyncHeight': 1220798,
# 				'successBlocks': 157650},
# 				'windowUptime': {'uptime': 0.9983918520503886,
# 				'windowStart': 1209601,
# 				'windowEnd': 1238400}},
# 				'rank': -1,
# 				'votingPowerPercent': 0.007113002117305917,
# 				'cumulativeShare': 0.8444542916044262,
# 				'eth': '0x3db128233554ce6bac5dcd7003644f540eb0e57c', 'moniker': 'ftp_validator', 'avatar': 'https://i.ibb.co/HGZNxPW/2024-04-08-14-44-28.png', 'banner': None, 'twitterUrl': 'https://x.com/solodanETH', 'githubUrl': 'https://github.com/Denend', 'webUrl': 'https://solodan.xyz', 'identity': None, 'securityContact': 'https://t.me/daniel_solo', 'details': 'FTP Validators since 2021'}, 'rewards': '25827669.539051520000000000'}