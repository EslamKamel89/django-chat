from typing import cast

from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render

from .forms import UserSettingsForm
from .models import Room


# Create your views here.
def index(request: HttpRequest):
    print(type(request))
    context = {"rooms": Room.objects.all()}
    return render(request, "index.html", context)


@login_required()
def room(request: HttpRequest, room_slug: str):
    room_model = get_object_or_404(Room, slug=room_slug)
    messages = cast(QuerySet, room_model.messages.select_related("user").order_by("created_at"))  # type: ignore
    return render(request, "room.html", {"room": room_model, "messages": messages})


@login_required()
def settings(request: HttpRequest):
    form = UserSettingsForm(instance=request.user)
    return render(
        request,
        "settings.html",
        {"form": form},
    )
