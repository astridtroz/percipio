from django.urls import path
from .views import chat_test_view
from . import consumers

urlpatterns = [
    path('test/', chat_test_view, name='chat-test'),
]

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
]



