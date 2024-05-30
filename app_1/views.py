

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import ConnexionUserForm

def accueil(request):
   return render(request, 'accueil.html')

def vue_connexion(request):
    if request.method == 'POST':
        form = ConnexionUserForm(request, data=request.POST)
        if form.is_valid():
            utilisateur = form.get_user()
            login(request, utilisateur)
            return redirect('vue_profile')
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
