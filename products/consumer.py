# from channels.generic.websocket import AsyncWebsocketConsumer
# import json

# class OrderConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def receive(self, text_data):
#         message = json.loads(text_data)
#         if message['type'] == 'new_order':
#             order = message['order']
#             # Send a notification to the admin here, for example using Django's built-in messaging framework
#             await self.send(text_data=json.dumps({'message': 'New order received!'}))


from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
import json

# channel_layer = get_channel_layer()

# class AdminNotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.channel_layer.group_add("admin_notifications", self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard("admin_notifications", self.channel_name)

#     async def notify_admins(self, event):
#         message = event["message"]
#         await self.send(text_data=json.dumps({
#             'type': 'notification',
#             'message': message,
#         }))

from channels.generic.websocket import AsyncWebsocketConsumer

class AdminNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("admin_notifications", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("admin_notifications", self.channel_name)

    async def notify_admins(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': message,
        }))
