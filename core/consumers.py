import json

from channels.generic.websocket import WebsocketConsumer

from core.models import Message, Room, User


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user: User = self.scope["user"]  # type: ignore
        if not self.user:
            self.close()
            return
        self.room_slug = self.scope["url_route"]["kwargs"]["room_slug"]  # type: ignore
        self.room = self.get_room()
        if not self.room:
            self.close()
            return
        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        if text_data != None:
            text_data_json = json.loads(text_data)
            message = text_data_json.get("message", None)
            if message != None:
                Message.objects.create(user=self.user, room=self.room, content=message)
                # todo: in the next lessons we will return proper htmx response from the server
                self.send(text_data=json.dumps({"message": message}))

    def get_room(self):
        return Room.objects.filter(slug=self.room_slug).first()
