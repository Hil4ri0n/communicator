from django.http import HttpResponse
from django.shortcuts import render
from users_and_profiles.models import Profile
from .models import ChatRoom


def chat(request, friend_id):
    friend_profile = Profile.objects.get(id=friend_id)
    chat_room = ChatRoom.objects \
        .filter(participants__id=request.user.profile.id) \
        .filter(participants__id=friend_id).first()

    if not chat_room:
        return HttpResponse("No chat room found.", status=404)

    received_messages = chat_room.messages.filter(sender_id=friend_id, viewed=False)
    received_messages.update(viewed=True)
    message_from_user = chat_room.get_last_viewed_message(request.user.profile.id)

    messages = chat_room.messages.all()
    context = {
        'messages': messages,
        'friend_profile': friend_profile,
        'message_from_user': message_from_user
    }
    return render(request, 'chat/chat.html', context)
