import asyncio
import websockets

class websocketClient():

    connection = 'no conncetion'
    name = 'no name'

    def __init__(self):
        pass

    #Creates a connection with the server and gets information about the client
    async def connect(self):
        print('Preparing to connect...')
        self.connection = await websockets.client.connect('ws://localhost:8765')
        print('Connected')
        self.name = input('Please insert your nickname ')
        await self.connection.send(self.name)
        print(f"> {self.name}")
        greeting = await self.connection.recv()
        print(f"< {greeting}")
        return self.connection

    #Always ready to take a message from the client and send it back to the server
    async def message(self):
        while True:
            try:
                message = input('>> ')
                await self.connection.send(message)
            except self.connection.exception.ConnectionClosed:
                print('Connection Closed')
                break

    #Always listens to the server for messages
    async def listen(self):
        while True:
            try:
                message = await self.connection.recv()
                print(f"< {message}")
            except self.connection.exception.ConnectionClosed:
                print('Connection closed')
                break

    #Listens for message and is ready to send message concurrently
    async def onConnect(self):
        await asyncio.gather(
            self.listen(),
            self.message(),
        )
