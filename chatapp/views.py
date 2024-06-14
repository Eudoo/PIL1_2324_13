from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from .models import Messages, Room
from app_1.models import Profile
from django.http import JsonResponse

# Create your views here.


def discussion(request):
    rooms = Profile.objects.exclude(utilisateur=request.user)
    return render(request, "chatapp/list.html", {'rooms': rooms})

def retour(request):
    return redirect('discussion')

def chat(request, username):
    user2 = get_object_or_404(User, username=username)
    profile2 = get_object_or_404(Profile, utilisateur=user2)
    user1 = request.user.profile.utilisateur

    chatRoom = Room.objects.filter(friends=user1).filter(friends=user2).first()
    if not chatRoom:
        chatRoom = Room.objects.create()
        chatRoom.friends.add(user1, user2)
        chatRoom.save()

    messages = Messages.objects.filter(chatRoom=chatRoom).order_by('date')

    if request.method == "POST":
        content = request.POST.get('contenu')
        if content:
            Messages.objects.create(chatRoom=chatRoom, sender=user1, receiver=user2, content=content)

    # Vérifier si la demande est effectuée via AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        last_message_id = request.GET.get('last_message_id')
        new_messages = Messages.objects.filter(chatRoom=chatRoom, id__gt=last_message_id).order_by('date')
        return render(request, 'chatapp/new_messages.html', {'messages': new_messages})

    return render(request, 'chatapp/room.html', {'chatRoom': chatRoom, 'messages': messages, 'user1': request.user, 'user2': user2, 'profile2': profile2})
