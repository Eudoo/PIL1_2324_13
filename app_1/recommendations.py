# recommendations.py

from .models import Profile

def recommander_partenaires(utilisateur):
    profil_utilisateur = Profile.objects.get(utilisateur=utilisateur)
    
    # Vérifie que l'âge de l'utilisateur actuel n'est pas None
    if profil_utilisateur.age is None:
        raise ValueError("L'âge de l'utilisateur actuel ne peut pas être None")

    age_utilisateur = profil_utilisateur.age
    sexe_utilisateur = profil_utilisateur.sexe
    interets_utilisateur = profil_utilisateur.interet.all()

    # Recherche des profils de partenaires potentiels
    profils = Profile.objects.exclude(utilisateur=utilisateur)
    recommandations = []

    for profil in profils:
        # Vérifie que l'âge du profil potentiel n'est pas None
        if profil.age is None:
            continue

        # Calcule une "distance" en fonction des caractéristiques
        age_difference = abs(profil.age - age_utilisateur)
        same_sexe = profil.sexe != sexe_utilisateur
        common_interests = len(set(interets_utilisateur).intersection(set(profil.interet.all())))

        # Vous pouvez ajuster les critères de sélection selon vos besoins
        if age_difference <= 5 and same_sexe and common_interests > 0:
            recommandations.append(profil)

    return recommandations
