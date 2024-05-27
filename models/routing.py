from django.urls import re_path
from .consumers import RealTimeConsumer

websocket_urlpatterns = [
    re_path(r'ws/realtime/$', RealTimeConsumer.as_asgi()),
]