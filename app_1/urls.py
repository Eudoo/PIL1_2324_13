from django.urls import path
from .views import vue_connexion, vue_deconnexion,vue_profile, accueil, vue_inscription1, vue_inscription2
from .views import vue_recommandations, vue_base, vue_recherche, vue_profile_partenaire, vue_like_profile, vue_modifier_profile
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', accueil, name='accueil'),
    path('connexion/', vue_connexion, name='vue_connexion'),
    path('mot_oublie', auth_views.PasswordResetView.as_view(template_name='mot_oublie.html'), name='vue_mot_oublie'),
    
    path('deconnexion/', vue_deconnexion, name='vue_deconnexion'),
    path('profile/', vue_profile, name='vue_profile'),
    path('inscription1/', vue_inscription1, name='vue_inscription1'),
    path('incription2/', vue_inscription2, name='vue_inscription2'),
    path('recommandations/', vue_recommandations, name='vue_recommandations'),
    path('base/', vue_base, name='vue_base'),
    path('recherche/', vue_recherche, name='vue_recherche'),
    path('profil/<str:username>/', vue_profile_partenaire, name='vue_profile_partenaire'),
    path('like/<int:user_id>/', vue_like_profile, name='vue_like_profile'),
    path('profile/modifier/', vue_modifier_profile, name='vue_modifier_profile'),
]