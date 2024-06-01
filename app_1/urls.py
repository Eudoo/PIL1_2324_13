from django.urls import path
from .views import vue_connexion, vue_deconnexion, vue_profile, accueil, vue_inscription1, vue_inscription2


urlpatterns = [
    path('', accueil, name='accueil'),
    path('connexion/', vue_connexion, name='vue_connexion'),
    path('deconnexion/', vue_deconnexion, name='vue_deconnexion'),
    path('profile/', vue_profile, name='vue_profile'),
    path('inscription1/', vue_inscription1, name='vue_inscription1'),
    path('incription2/', vue_inscription2, name='vue_inscription2'),
]