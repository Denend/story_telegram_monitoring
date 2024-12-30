# test

import requests # в оффке aiohttp

va = "storyvaloper1rxa60lwchrr0mzsrwqud6rrz6jgdat7gsglmet"
url = "https://api.testnet.storyscan.app/validators/" + va

data = requests.get(url).json()
historical_uptime = data["uptime"]["historicalUptime"]

earliestHeight = historical_uptime["earliestHeight"]
lastSyncHeight = historical_uptime["lastSyncHeight"]
successBlocks = historical_uptime["successBlocks"]

totalBlocks = lastSyncHeight - earliestHeight

# totalMissedPercent = 100 - (totalMissedBlocks / successBlocks * 100)
historicalUptime = (successBlocks / (lastSyncHeight - earliestHeight)) * 100

print(historical_uptime)
print(totalMissedBlocks, historicalUptime)
