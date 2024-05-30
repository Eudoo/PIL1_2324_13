from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

Utilisateur = get_user_model()

class Pseudo_Email_Backend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            utilisateur = Utilisateur.objects.get(pseudo=username)
        except Utilisateur.DoesNotExist:
            try:
                utilisateur = Utilisateur.objects.get(email=username)
            except Utilisateur.DoesNotExist:
                return None

        if utilisateur.check_password(password):
            return utilisateur

        return None

    def get_user(self, user_id):
        try:
            return Utilisateur.objects.get(pk=user_id)
        except Utilisateur.DoesNotExist:
            return None
