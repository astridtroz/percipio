from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/private-chat/<str:name>/', consumers.PrivateChatConsumer.as_asgi()),
    path('ws/project-chat/<int:project_id>/', consumers.ProjectGroupChatConsumer.as_asgi()),
]
