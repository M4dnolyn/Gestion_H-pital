from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import role_required
from .forms import UserCreationForm

@login_required
@role_required(['ADMIN', 'DIR']) # Autoriser Admin Système et Direction
def admin_create_user(request):
    """Vue pour qu'un administrateur puisse créer un compte utilisateur"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Le compte utilisateur '{user.username}' a été créé avec succès !")
            return redirect('admin_create_user')
    else:
        form = UserCreationForm()
    
    return render(request, 'core/user_create.html', {
        'form': form,
        'title': 'Créer un utilisateur'
    })
