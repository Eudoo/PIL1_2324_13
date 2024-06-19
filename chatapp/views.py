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

def notifications(request):
    return render(request, 'chatapp/notifs.html')

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

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        last_message_id = request.GET.get('last_message_id')
        new_messages = Messages.objects.filter(chatRoom=chatRoom, id__gt=last_message_id).order_by('date')
        return render(request, 'chatapp/new_messages.html', {'messages': new_messages})

    return render(request, 'chatapp/room.html', {'chatRoom': chatRoom, 'messages': messages, 'user1': request.user, 'user2': user2, 'profile2': profile2})

def get_notifications(request):

    latest_received_messages = Messages.objects.filter(receiver=request.user).exclude(sender=request.user).order_by('-date')[:10]

    notifications = []
    for message in latest_received_messages:
        notifications.append({
            'sender': message.sender.username,
            'content': message.content,
            'date': message.date.strftime('le %d-%m à %H:%M:%S'),
        })

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'notifications': notifications})
    else:
        return render(request, 'chatapp/notifs.html', {'notifications': notifications})
