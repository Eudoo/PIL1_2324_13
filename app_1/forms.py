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
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_first_name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_last_name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'id_email'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        mot_de_passe = cleaned_data.get("mot_de_passe")
        confirmation_mot_de_passe = cleaned_data.get("confirmation_mot_de_passe")

        if mot_de_passe != confirmation_mot_de_passe:
            raise forms.ValidationError("Les mots de passe ne correspondent pas!")
        return cleaned_data

class Inscription2Form(forms.ModelForm):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    age = forms.IntegerField(required=True, label="Âge", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    sexe = forms.ChoiceField(choices=[('Homme', 'Homme'), ('Femme', 'Femme'), ('Autre', 'Autre')], widget=forms.Select(attrs={'class': 'form-control'}))
    interet = forms.ModelMultipleChoiceField(queryset=Interest.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}), required=True)
    photo_de_profil = forms.ImageField(required=True, widget=forms.FileInput(attrs={'class': 'form-control'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}), required=True)
    localisation = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    
    class Meta:
        model = Profile
        fields = ['username','age', 'sexe', 'interet', 'photo_de_profil', 'bio', 'localisation']

    interet = forms.ModelMultipleChoiceField(queryset=Interest.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}), required=True)
    photo_de_profil = forms.ImageField(required=True, widget=forms.FileInput(attrs={'class': 'form-control'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}), required=True)
    localisation = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)

    def __init__(self, *args, **kwargs):
        super(Inscription2Form, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['age'].widget.attrs.update({'class': 'form-control'})
        self.fields['sexe'].widget.attrs.update({'class': 'form-control'})
        self.fields['interet'].widget.attrs.update({'class': 'form-control'})
        self.fields['photo_de_profil'].widget.attrs.update({'class': 'form-control'})
        self.fields['bio'].widget.attrs.update({'class': 'form-control'})
        self.fields['localisation'].widget.attrs.update({'class': 'form-control'})
    
class ConnexionUserForm(forms.Form):
    pseudo = forms.CharField(label='Pseudo', widget=forms.TextInput(attrs={'class': 'form-control'}))
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

class RechercheForm(forms.Form):
    q = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Rechercher un utilisateur', 'class': 'form-control'}), label='')
    ville = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Spécifier une ville', 'class': 'form-control'}), label='')
    sexe = forms.ChoiceField(required=False, choices=[('', 'Sélectionnez le sexe'), ('Homme', 'Homme'), ('Femme', 'Femme'), ('Autre', 'Autre')], widget=forms.Select(attrs={'class': 'form-control'}), label='')
    interets = forms.ModelMultipleChoiceField(queryset=Interest.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}), label='Sélectionnez les intérêts', required=False)

    def __init__(self, *args, **kwargs):
        super(RechercheForm, self).__init__(*args, **kwargs)
        self.fields['interets'].queryset = Interest.objects.all()

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['age', 'sexe', 'bio', 'localisation', 'interet', 'photo_de_profil']
        widgets = {
            'interet': forms.CheckboxSelectMultiple(),
        }

class UserProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = Profile
        fields = ['username', 'email', 'age', 'sexe', 'bio', 'localisation', 'interet', 'photo_de_profil']
        widgets = {
            'interet': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        user = super(UserProfileForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user