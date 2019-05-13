import asyncio
import websockets
from collections import namedtuple
import threading

Clients = namedtuple("Clients", "name ws")
connectedClients = set()

# Sends everybody in the group a message when someone joins the chat
async def notify_in(name):
    if connectedClients:
        message = name + ' has joined the chat room.'
        await asyncio.wait([clients.ws.send(message) for clients in connectedClients])


# Sends everybody in the group a message when someone leaves the chat
async def notify_out(name):
    if connectedClients:
        message = name + ' has left the chat room.'
        await asyncio.wait([clients.ws.send(message) for clients in connectedClients])

# Registers the user with a nickname and their websocket address
async def register(websocket, name):
    client = Clients(name, websocket)
    connectedClients.add(client)
    await notify_in(name)

# Unregisters the user by removing their nickname and websocket address
async def unregister(name):
    for client in connectedClients:
        if client.name == name:
            connectedClients.remove(client)
    await notify_out(name)

# initiate contact with
async def initiate(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")
    greeting = f"Hello {name}, please send your message!"
    await register(websocket, name)
    await websocket.send(greeting)
    print(f"> {greeting}")

    # This function does not handle concurrency. Need to fix

async def recvMessage():
    for websocket in connectedClients:
        message = await websocket.recv()
        return message

async def sendMessage(message):
    for websocket in connectedClients:
        await websocket.send(message)
    # await asyncio.wait([websocket.send(message) for websocket in .connectedClients])

async def listen():
    while True:
        message = await recvMessage()
        await sendMessage(message)

# class Client(threading.Thread):
#     def __init__(self, nickname, websocket):
#         super(Client, self).__init__()
#         self.nickname = nickname
#         self.websocket = websocket
#
#     async def run(self):
#         while True:
#             message = await self.websocket.recv()
#
#
#             message = await recvMessage()
#             await sendMessage(message)


start_server = websockets.serve(initiate, 'localhost', 8765)
asyncio.get_event_loop().run_until_complete(start_server)
#asyncio.get_event_loop().run_until_complete(listen())
print("1")
asyncio.get_event_loop().run_forever()

