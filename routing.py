# routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path

from .consumers import VoiceCommandConsumer

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        re_path(r'ws/voice_command/$', VoiceCommandConsumer.as_asgi()),
    ]),
})
