from django.contrib import admin
from unfold.admin import ModelAdmin

from core.models import Message, Room

# Register your models here.


@admin.register(Room)
class RoomAdmin(ModelAdmin):
    pass


@admin.register(Message)
class MessageAdmin(ModelAdmin):
    pass
