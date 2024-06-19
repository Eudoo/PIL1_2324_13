from django.urls import path
from chatapp.views import discussion, get_notifications, retour, chat, notifications

urlpatterns = [
    path('discussion/', discussion, name="discussion"),
    path('discussion/', retour, name="retour"),
    path('chat/<str:username>/', chat, name="chat"),
    path('notifications/', notifications, name='notifications'),
    path('get_notifications/', get_notifications, name='get_notifications'),
]
