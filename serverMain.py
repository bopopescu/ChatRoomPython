import websocketServer
import websockets
import asyncio

print('Preparing to connect')
start_server = websockets.serve(initiate, 'localhost', 8765)
print('Connected')
asyncio.get_event_loop().run_until_complete(start_server)
print('Not suppose to go here')
asyncio.get_event_loop().run_until_complete(listen())
print('Finished listening')


