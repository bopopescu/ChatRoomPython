from websocketClient import websocketClient
import asyncio

name = input("What is your nickname? ")
user = websocketClient(name)
loop = asyncio.get_event_loop()
loop.run_until_complete(user.connect())
loop.run_forever()


