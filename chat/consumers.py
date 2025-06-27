import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from user.models import MyUser
from .models import PrivateChatMessage, ProjectGroupChatMessage
from tasks.models import Project



class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = None  # Avoid attribute error during disconnect

        if isinstance(self.scope["user"], AnonymousUser):
            await self.close()
            return

        self.other_user = self.scope['url_route']['kwargs']['name']
        current_user_name = self.scope['user'].name
        self.room_name = f"private_{min(current_user_name, self.other_user)}_{max(current_user_name, self.other_user)}"

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Only attempt group discard if connection was accepted and room_name is set
        if hasattr(self, 'room_name') and self.room_name:
            await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender = self.scope["user"]

        receiver = await database_sync_to_async(MyUser.objects.get)(name=self.other_user)
        await database_sync_to_async(PrivateChatMessage.objects.create)(
            sender=sender,
            receiver=receiver,
            message=message
        )

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.name
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

class ProjectGroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 🔒 Block anonymous users
        if isinstance(self.scope["user"], AnonymousUser):
            await self.close()
            return

        self.project_id = self.scope['url_route']['kwargs']['project_id']
        self.user = self.scope['user']
        self.room_group_name = f'project_{self.project_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # 💾 Save group message
        await self.save_group_message(self.project_id, self.user, message)

        # 📤 Broadcast message
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'group_chat_message',
                'message': message,
                'sender': self.user.name
            }
        )

    async def group_chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender']
        }))

    @database_sync_to_async
    def save_group_message(self, project_id, sender, message):
        project = Project.objects.get(id=project_id)
        return ProjectGroupChatMessage.objects.create(
            project=project,
            sender=sender,
            message=message
        )
