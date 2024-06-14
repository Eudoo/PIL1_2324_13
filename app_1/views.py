from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import Inscription1Form, Inscription2Form, ConnexionUserForm
from .recommendations import recommander_partenaires
from .models import Like

User = get_user_model()

def accueil(request):
    return render(request, 'accueil.html')


def vue_inscription1(request):
    if request.method == 'POST':
        form = Inscription1Form(request.POST)
        if form.is_valid():
            request.session['registration_data'] = form.cleaned_data
            return redirect('vue_inscription2')
    else:
        form = Inscription1Form()
    return render(request, 'inscription1.html', {'form': form})


def vue_inscription2(request):
    if 'registration_data' not in request.session:
        return redirect('vue_inscription1')
    
    if request.method == 'POST':
        form = Inscription2Form(request.POST, request.FILES)
        if form.is_valid():
            registration_data = request.session.pop('registration_data')
            username = form.cleaned_data['username']
            user = User.objects.create_user(
                username=username,
                email=registration_data['email'],
                first_name=registration_data['first_name'],
                last_name=registration_data['last_name'],
                password=registration_data['mot_de_passe'],  
            )

            profile = form.save(commit=False)
            profile.utilisateur = user
            profile.save()
            form.save_m2m() 

            backend = 'django.contrib.auth.backends.ModelBackend'

            login(request, user, backend=backend)
            return redirect('vue_connexion')
    else:
        form = Inscription2Form()
    return render(request, 'inscription2.html', {'form': form})


def vue_connexion(request):
    if request.method == 'POST':
        form = ConnexionUserForm(request.POST)
        if form.is_valid():
            utilisateur = form.get_user()
            if utilisateur is not None:
                login(request, utilisateur)
                return redirect('vue_base')
            else:
                print("Utilisateur non trouvé")
        else:
            print("Formulaire invalide : ", form.errors)
    else:
        form = ConnexionUserForm()
    return render(request, 'connexion.html', {'form': form})

def vue_deconnexion(request):
    logout(request)
    return redirect('vue_connexion')

def vue_profile(request):
    return render(request, 'profile.html', {'utilisateur': request.user})

def vue_recommandations(request):
    utilisateur = request.user
    recommandations = recommander_partenaires(utilisateur)

    recommandations_data = []
    for recommandation in recommandations:
        has_liked = Like.objects.filter(liker=request.user, liked=recommandation.utilisateur).exists()
        recommandations_data.append((recommandation, has_liked))
        
    return render(request, 'recommandations.html', {'recommandations_data':recommandations_data})

@login_required
def vue_base(request):
    return render(request, 'base.html')

def vue_recherche(request):
    query = request.GET.get('q')
    if query:
        results = User.objects.filter(username__icontains=query)
    else:
        results = User.objects.none()
    return render(request, 'recherche.html', {'results':results, 'query':query})

def vue_profile_partenaire(request, username):
    utilisateur = get_object_or_404(User, username=username)
    return render(request, 'profile_partenaire.html', {'utilisateur': utilisateur})

def vue_like_profile(request, user_id):
    user_to_like = get_object_or_404(User, id=user_id)
    like, created = Like.objects.get_or_create(liker=request.user, liked=user_to_like)
    if not created:
        like.delete()
    return redirect('vue_recommandations')
