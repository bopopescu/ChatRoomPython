import asyncio
import websockets

class websocketClient():

    connection = 'no connection'
    name = 'no name'

    def __init__(self, nickname):
        self.name = nickname

    #Creates a connection with the server and gets information about the client
    async def connect(self):
        async with websockets.connect("ws://localhost:8765") as socket:
            message = input('Please send your message: ')
            message = self.name + " ::: " + message
            await socket.send(message)
            print(f"> {message}")
            confirmation = await socket.recv()
            print(f"< {confirmation}")

        # print('Preparing to connect...')
        # self.connection = await websockets.client.connect('ws://localhost:8765')
        # print('Connected')
        # while True:

    #Always ready to take a message from the client and send it back to the server
    # async def message(self):
    #     while True:
    #         try:
    #             message = input('>> ')
    #             await self.connection.send(message)
    #         except self.connection.exception.ConnectionClosed:
    #             print('Connection Closed')
    #             break
    #
    # #Always listens to the server for messages
    # async def listen(self):
    #     while True:
    #         try:
    #             message = await self.connection.recv()
    #             print(f"< {message}")
    #         except self.connection.exception.ConnectionClosed:
    #             print('Connection closed')
    #             break
    #
    # #Listens for message and is ready to send message concurrently
    # async def onConnect(self):
    #     await asyncio.gather(
    #         self.listen(),
    #         self.message(),
    #     )
