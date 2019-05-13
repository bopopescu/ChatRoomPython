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
    for client in connectedClients:
        message = await client.ws.recv()
        return message

async def sendMessage(message):
    for client in connectedClients:
        await client.ws.send(message)
    await asyncio.wait([client.ws.send(message) for client in connectedClients])

async def listen():
    while True:
        message = await recvMessage()
        await sendMessage(message)

start_server = websockets.serve(initiate, 'localhost', 8765)
loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(start_server)
    asyncio.ensure_future(listen())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Closing Loop")
    loop.close()

