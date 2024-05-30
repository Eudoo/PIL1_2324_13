from django.urls import path
from .views import vue_connexion, vue_deconnexion, vue_profile, accueil


urlpatterns = [
    path('', accueil, name='accueil'),
    path('connexion/', vue_connexion, name='vue_connexion'),
    path('deconnexion/', vue_deconnexion, name='vue_deconnexion'),
    path('profile/', vue_profile, name='vue_profile'),
]