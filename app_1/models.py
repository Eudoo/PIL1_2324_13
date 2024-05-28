from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Utilisateur(AbstractUser):
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)


class Profile(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    date_naissance = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    localisation = models.CharField(max_length=70)
    interet = models.ManyToManyField('Interest', blank=True)
    photo_de_profil = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self) :
        return self.utilisateur.username


class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    contenu = models.TextField()
    expediteur = models.ForeignKey(Utilisateur, related_name='envoie_les_messages', on_delete=models.CASCADE)
    destinataire = models.ForeignKey(Utilisateur, related_name='recoit_les_messages', on_delete=models.CASCADE)
    heure_d_envoie = models.DateTimeField(auto_now=True)
    conversation = models.ForeignKey('Conversation', related_name='messages', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.expediteur.username} to {self.destinataire.username}: {self.contenu[:20]}'

