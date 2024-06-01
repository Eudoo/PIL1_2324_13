from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Profile, Interest
from django.contrib.auth import get_user_model

Utilisateur = get_user_model()

class Inscription1Form(forms.ModelForm):
    mot_de_passe = forms.CharField(widget=forms.PasswordInput)
    confirmation_mot_de_passe = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        mot_de_passe = cleaned_data.get("mot_de_passe")
        confirmation_mot_de_passe = cleaned_data.get("confirmation_mot_de_passe")

        if mot_de_passe != confirmation_mot_de_passe:
            raise forms.ValidationError("Les mots de passe ne correspondent pas!")
        return cleaned_data

class Inscription2Form(forms.ModelForm):

    username = forms.CharField(max_length=50)
    age = forms.IntegerField(required=True, label="Age")

    class Meta:
        model = Profile
        fields = ['age', 'sexe', 'interet', 'photo_de_profil']

    interet = forms.ModelMultipleChoiceField(queryset=Interest.objects.all(), widget=forms.CheckboxSelectMultiple, required=True)
    photo_de_profil = forms.ImageField(required=True)

    def __init__(self, *args, **kwargs):
        super(Inscription2Form, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['age'].widget.attrs.update({'class': 'form-control'})
        self.fields['sexe'].widget.attrs.update({'class': 'form-control'})
        self.fields['interet'].widget.attrs.update({'class': 'form-control'})
        self.fields['photo_de_profil'].widget.attrs.update({'class': 'form-control'})

        self.fields = {
            'username': self.fields['username'],
            'age': self.fields['age'],
            'sexe': self.fields['sexe'],
            'interet': self.fields['interet'],
            'photo_de_profil': self.fields['photo_de_profil'],
        }

class ConnexionUserForm(forms.Form):
    pseudo = forms.CharField(label='Pseudo ou Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    mot_de_passe = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        pseudo_email = cleaned_data.get('pseudo')
        mot_de_passe = cleaned_data.get('mot_de_passe')

        if pseudo_email and mot_de_passe:
            # Authentification par pseudo ou email
            user = authenticate(username=pseudo_email, password=mot_de_passe)
            if user is None:
                try:
                    user = Utilisateur.objects.get(email=pseudo_email)
                    if not user.check_password(mot_de_passe):
                        raise forms.ValidationError("Mot de passe incorrect")
                    user = authenticate(username=user.username, password=mot_de_passe)
                except Utilisateur.DoesNotExist:
                    raise forms.ValidationError("Pseudo ou Email incorrect")
            self.user_cache = user
        else:
            raise forms.ValidationError("Veuillez entrer à la fois le pseudo/email et le mot de passe")

        if self.user_cache is None:
            raise forms.ValidationError("Impossible de se connecter avec les informations fournies.")

        return cleaned_data

    def get_user(self):
        return self.user_cache