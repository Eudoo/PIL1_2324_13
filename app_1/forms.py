from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

Utilisateur = get_user_model()

class ConnexionUserForm(AuthenticationForm):
    pseudo = forms.CharField(label='Pseudo ou Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    mot_de_passe = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        pseudo_email = self.cleaned_data.get('pseudo')
        mot_de_passe = self.cleaned_data.get('mot_de_passe')

        if pseudo_email and mot_de_passe:
            self.user_cache = None
            # Authentification par pseudo
            try:
                self.user_cache = Utilisateur.objects.get(username=pseudo_email)
            except Utilisateur.DoesNotExist:
                # Authentification par email
                try:
                    self.user_cache = Utilisateur.objects.get(email=pseudo_email)
                except Utilisateur.DoesNotExist:
                    raise forms.ValidationError("Pseudo ou Email incorrect")

            if self.user_cache:
                if not self.user_cache.check_password(mot_de_passe):
                    raise forms.ValidationError("Mot de passe incorrect")
        else:
            raise forms.ValidationError("Veuillez entrer à la fois le pseudo/email et le mot de passe")

        return self.cleaned_data

    def get_user(self):
        return self.user_cache
