import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self): 
        # function that connects user to server via websocket connection and channel layer helps to add room in the group
        self.room_name= self.scope['url_route']['kwargs']['room_name']
        self.room_group_name= f'chat_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
    
    async def disconnect(self, code):
        #remove connection
        return await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    
    async def receive(self,text_data):
        #when user sends message call chat message to send the message to each user connected with same group by channel layer
        text= json.loads(text_data)
        message= text['message']
        username= self.scope["user"].name

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message': message,
                'username': username,
            }
        )
    
    async def chat_message(self,event):
        await self.send(text_data=json.dumps(
            {
                'message': event['message'],
                'username':event['username'],
            }
        ))