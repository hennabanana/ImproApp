import asyncio # new

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .serializer import TaskSerializer
import json


#Consumer des Channels
class ImproConsumer(AsyncJsonWebsocketConsumer):
    #init des ImproConsumer
    def __init__(self, scope):
            super().__init__(scope)
            self.user_group_name = ''
            self.game_group_name = 'Player'
    async def connect(self):
        actor = False
        #wenn in der url eine Variable in kwargs mitgegeben wurde
        if 'userid' in self.scope['url_route']['kwargs']:
            #es wird die id aus der URL gezogen
            userid = self.scope['url_route']['kwargs']['userid']
            #der consumer user bekommt die id gesetzt
            self.user = userid
            #der user wird der gruppe notif_room_for_user_ + seine id
            #hinzugefügt
            self.user_group_name = "notif_room_for_user_"+str(self.user) 
            #die variable wird auf True gesetzt da es sich um ein Actor handelt
            actor = True
            #der benutzer wird der gruppe und dem Channel hinzugefügt
            await self.channel_layer.group_add(
                self.user_group_name,
                self.channel_name
                )
        else:
            #befindet sich keine variable in der URL
            #wird der Benutzer der Gruppe Player hinzugeüfgt
            self.game_group_name = 'Player'
            #der benutzer wird der gruppe und dem Channel hinzugefügt
            await self.channel_layer.group_add(
                self.game_group_name,
                self.channel_name
            )
        #mit dem self.accept() wird die Verbindung mit dem Client
        #akzeptiert und hergestellt
        await self.accept()
        #falls es sich um ein Actor handelt muss nach dem
        #connect die Liste der Actors aktualisiert werden
        #so wird die Gruppe Player benachrichtigt dass sie 
        #die liste neu laden soll
        if actor:
            updateActor = '{"type":"update.actor"}'
            await self.receive(updateActor)



    async def disconnect(self, close_code):
        # bei einem disconnect (logout)
        # werden die user aus der gruppe 
        # und dem channel entfernt
        if self.user_group_name:
            await self.channel_layer.group_discard(
                self.user_group_name,
                self.channel_name
            )
        else:
            await self.channel_layer.group_discard(
                self.game_group_name,
                self.channel_name
            )
    # Methode wir bei eingehenden nachrichten 
    # aufgerufen
    async def receive(self, text_data):
        #text_data wird encodet
        text_data_json = json.loads(text_data)
        #der typ wird aus der nachricht geholt
        type = text_data_json['type']
        if type == 'update.task':
            # Seine benachrichtigung wird an die gruppe gesendet
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'update_task',
                }
            )
        if type == 'update.actor':
            # Seine benachrichtigung wird an die gruppe gesendet
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'update_actor',
                }
            )
        if type == 'create.task':
            # Send message to room group
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'create_task',
                }
            )
        if type == 'logout':
            # Send message to room group
            await self.disconnect("logout")
        if type == 'readout.task':
            #task wird ausgelesen
            task = text_data_json['task']
            #das dict wird kopiert
            task_actors = dict(task)
            #die liste der actors wird gepopt
            actors_data = task_actors.pop('actors')
            actors = []
            for actor_data in actors_data:
                    #userdaten werden geholt
                    user_data = actor_data.get('user')
                    userid = user_data.get('id')
                    #ids werden der actors-liste hinzugefügt
                    actors.append(userid)
            #die liste der actors wird iteriert
            for userid in actors:
                #die passenden actor-gruppen werden anhand
                #der id benachrichtig dass die Aufgabe
                #vorgelesen werden soll
                group = "notif_room_for_user_"+str(userid)
                await self.channel_layer.group_send(
                    group=group, message=
                    {
                        'type': 'readout_task',
                        'task': task
                    }
                )

    # methode von gruppenanruf wird aufgerufen
    async def create_task(self, event):
        # Nachricht wird zum websocket gesendet
        await self.send(text_data=json.dumps({
            'update': 'task'
        }))
    # methode von gruppenanruf wird aufgerufen
    async def update_task(self, event):
        # Nachricht wird zum websocket gesendet
        await self.send(text_data=json.dumps({
            'update': 'task'
        }))
    # methode von gruppenanruf wird aufgerufen
    async def update_actor(self, event):
        # Nachricht wird zum websocket gesendet
        await self.send(text_data=json.dumps({
            'update': 'actor'
        }))
    # methode von gruppenanruf wird aufgerufen
    async def readout_task(self, event):
        task = event['task']
        # Nachricht wird zum websocket gesendet
        await self.send(text_data=json.dumps({
            'task': task
        }))
   