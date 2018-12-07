from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

import json 

from .models import Dealer


class DealerConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = "dealers"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        name = text_data_json["name"]
        decks = text_data_json["decks"]
        id = text_data_json["id"]

        dealer = Dealer.objects.get(pk=id)
        dealer.name = name
        dealer.decks = decks
        dealer.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "add_dealer",
                "name": name,
                "decks": decks,
                "id": id
            }
        )

    def add_dealer(self, event):
        name = event["name"]
        decks = event["decks"]
        id = event["id"]
        self.send(text_data=json.dumps({
            "name": name,
            "decks": decks,
            "id": id
        }))
