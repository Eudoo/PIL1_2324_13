from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    sexe = models.CharField(max_length=8, choices=[('Homme', 'Homme'), ('Femme', 'Femme'), ('Autre', 'Autre')], null=True)
    bio = models.TextField(blank=True)
    localisation = models.CharField(max_length=70, blank=True)
    interet = models.ManyToManyField('Interest', blank=True)
    photo_de_profil = models.ImageField(upload_to='profile_pictures', null=True)

    def __str__(self) :
        return self.utilisateur.username


class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    contenu = models.TextField()
    expediteur = models.ForeignKey(User, related_name='envoie_les_messages', on_delete=models.CASCADE)
    destinataire = models.ForeignKey(User, related_name='recoit_les_messages', on_delete=models.CASCADE)
    heure_d_envoie = models.DateTimeField(auto_now=True)
    conversation = models.ForeignKey('Conversation', related_name='messages', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.expediteur.username} to {self.destinataire.username}: {self.contenu[:20]}'


class Conversation(models.Model):
    intervenants = models.ManyToManyField(User, related_name='conversations')
    demarree_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Conversation entre {", ".join(utilisateur.username for utilisateur in self.intervenants.all())}'
    
class Like(models.Model):
    liker = models.ForeignKey(User, related_name='like_donné', on_delete=models.CASCADE)
    liked = models.ForeignKey(User, related_name='like_recu', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('liker', 'liked')

    def __str__(self):
        return f'{self.liker.username} likes {self.liked.username}'