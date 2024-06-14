from django.urls import path
from chatapp.views import discussion, retour, chat

urlpatterns = [
    path('discussion/', discussion, name="discussion"),
    path('discussion/', retour, name="retour"),
    path('chat/<str:username>/', chat, name="chat"),
]
