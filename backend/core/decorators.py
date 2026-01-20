from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def role_required(allowed_roles=[]):
    """
    Décorateur pour restreindre l'accès aux utilisateurs ayant un certain rôle.
    Redirige vers le dashboard avec un message d'erreur si l'accès est refusé.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Si superuser, accès toujours autorisé
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Vérifier si l'utilisateur a un profil personnel
            if hasattr(request.user, 'personnel_profile'):
                fonction = request.user.personnel_profile.fonction
                if fonction in allowed_roles:
                    return view_func(request, *args, **kwargs)
            
            # Accès refusé
            messages.error(request, "Accès non autorisé ! Vous n'avez pas les droits nécessaires pour accéder à cette page.")
            return redirect('dashboard')
            
        return _wrapped_view
    return decorator
