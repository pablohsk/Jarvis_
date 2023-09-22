# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class VoiceCommandConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        command_data = json.loads(text_data)
        command = command_data['command']

        # Aqui você pode processar o comando de voz e realizar ações com base nele.
        # Por exemplo, você pode chamar uma função que execute a funcionalidade desejada.

        # Após processar o comando, você pode enviar uma resposta de volta ao cliente (se necessário).

        await self.send(json.dumps({
            'message': 'Comando de voz recebido com sucesso!',
        }))
