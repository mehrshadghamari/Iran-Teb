import imp
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class AppointmentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('doctor_id',self.channel_name)
        await self.accept()
    

    async def disconnect(self, code):
         await self.channel_layer.group_discard('doctor_id',self.channel_name)


    async def send_action_appointment(self,event):
        new_data= event['text']
        await self.send(new_data)