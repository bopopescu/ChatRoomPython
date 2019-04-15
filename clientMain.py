from websocketClient import websocketClient
import asyncio

user = websocketClient()
loop = asyncio.get_event_loop()
connection = loop.run_until_complete(user.connect())
asyncio.run(user.onConnect())


