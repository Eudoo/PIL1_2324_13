from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import Inscription1Form, Inscription2Form, ConnexionUserForm, RechercheForm, UserProfileForm
from .recommendations import recommander_partenaires
from .models import Like, Profile, Interest

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
                messages.error(request, "Erreur d'authentification. Veuillez réessayer.")
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = ConnexionUserForm()
    return render(request, 'connexion.html', {'form': form})

@login_required
def vue_deconnexion(request):
    logout(request)
    return redirect('vue_connexion')

@login_required
def vue_profile(request):
    return render(request, 'profile.html', {'utilisateur': request.user})

@login_required
def vue_recommandations(request):
    form = RechercheForm()
    utilisateur = request.user
    recommandations = recommander_partenaires(utilisateur)

    recommandations_data = []
    for recommandation in recommandations:
        has_liked = Like.objects.filter(liker=request.user, liked=recommandation.utilisateur).exists()
        recommandations_data.append((recommandation, has_liked))

    return render(request, 'recommandations.html',{'form': form, 'recommandations_data':recommandations_data})

@login_required
def vue_base(request):
    form = RechercheForm()
    return render(request, 'base.html',{'utilisateur': request.user, 'form': form})

@login_required
def vue_recherche(request):
    form = RechercheForm(request.GET or None)
    results = Profile.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('q')
        ville = form.cleaned_data.get('ville')
        sexe = form.cleaned_data.get('sexe')
        interets = form.cleaned_data.get('interets')

        if query:
            results = results.filter(utilisateur__username__icontains=query)
        if ville:
            results = results.filter(localisation__icontains=ville)
        if sexe:
            results = results.filter(sexe=sexe)
        if interets:
            results = results.filter(interet__in=interets).distinct()

    return render(request, 'recherche.html', {'results': results,'form': form,})

@login_required
def vue_profile_partenaire(request, username):
    utilisateur = get_object_or_404(User, username=username)
    return render(request, 'profile_partenaire.html', {'utilisateur': utilisateur})

@login_required
def vue_like_profile(request, user_id):
    user_to_like = get_object_or_404(User, id=user_id)
    like, created = Like.objects.get_or_create(liker=request.user, liked=user_to_like)
    if not created:
        like.delete()
    return redirect('vue_recommandations')

@login_required
def vue_modifier_profile(request):
    profile = Profile.objects.get(utilisateur=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            request.user.username = form.cleaned_data['username']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            return redirect('vue_profile')
    else:
        form = UserProfileForm(instance=profile, user=request.user)
    return render(request, 'modifier_profile.html', {'form': form})