from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import Inscription1Form, Inscription2Form, ConnexionUserForm

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
                return redirect('vue_profile')
            else:
                print("Utilisateur non trouvé")
        else:
            print("Formulaire invalide : ", form.errors)
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
