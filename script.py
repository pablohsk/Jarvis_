import asyncio
import websockets
import json

async def send_voice_command():
    async with websockets.connect("ws://localhost:8000/ws/voice_command/") as websocket:
        command = {
            'command': 'Aqui está o seu comando de voz...'
        }
        await websocket.send(json.dumps(command))
        response = await websocket.recv()
        print(response)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(send_voice_command())
