import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.template.loader import render_to_string

from core.models import Message, Room, User


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user: User = self.scope["user"]  # type: ignore
        if not self.user.is_authenticated:
            self.close()
            return
        self.room_slug = self.scope["url_route"]["kwargs"]["room_slug"]  # type: ignore
        self.room = self.get_room()
        if not self.room:
            self.close()
            return
        # print("channel_layer: ", self.channel_layer)
        # print("channel_name: ", self.channel_name)
        self.room_group_name = f"chat_{self.room_slug}"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        if text_data is not None:
            text_data_json = json.loads(text_data)
            message = text_data_json.get("message", None)
            if message is not None:
                message_model = Message.objects.create(
                    user=self.user, room=self.room, content=message
                )
                # self.send(text_data=json.dumps({"message": message}))
                html = render_to_string(
                    "partials/message.html",
                    {"message": message_model, "user": self.user},
                )
                # self.send(text_data=html)
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name, {"type": "chat_message", "html": html}
                )

    def chat_message(self, event):
        html = event["html"]
        self.send(text_data=html)

    def get_room(self):
        return Room.objects.filter(slug=self.room_slug).first()
