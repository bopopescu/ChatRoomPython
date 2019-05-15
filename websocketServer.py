import asyncio
import websockets
from collections import namedtuple
import threading

connectedClients = set()

# Sends everybody in the group a message when someone joins the chat
async def notify_in(name):
    if connectedClients:
        message = name + ' has joined the chat room.'
        await asyncio.wait([clients.send(message) for clients in connectedClients])

# Sends everybody in the group a message when someone leaves the chat
async def notify_out(websocket, name):
    if connectedClients:
        message = name + ' has left the chat room.'
        await asyncio.wait([clients.send(message) for clients in connectedClients])

# Registers the user with a nickname and their websocket address
async def register(websocket, name):
    if websocket not in connectedClients:
        connectedClients.add(websocket)
        await notify_in(name)

# Unregisters the user by removing their nickname and websocket address
async def unregister(websocket, name):
    for client in connectedClients:
        if client == websocket:
            connectedClients.remove(client)
    await notify_out(websocket, name)

# initiate contact with
async def initiate(websocket, path):
    while True:
        print("Waiting...")
        message = await websocket.recv()
        name = message.partition(":")[0]
        await register(websocket, name)
        confirmation = "Message received"
        print(f"< {message}")
        await websocket.send(confirmation)


# async def recvMessage():
#     for client in connectedClients:
#         message = await client.ws.recv()
#         return message
#
# async def sendMessage(message):
#     for client in connectedClients:
#         await client.ws.send(message)
#
# async def listen():
#     print("Listening...")
#     message = await recvMessage()
#     print("Received message")
#     await sendMessage(message)
#     print("Sent message")

start_server = websockets.serve(initiate, 'localhost', 8765)

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(start_server)
    loop.run_forever()
finally:
    print("Closing Loop")
    loop.close()

