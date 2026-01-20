#!/usr/bin/env python
"""
Script pour réinitialiser le mot de passe du superutilisateur admin.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Réinitialiser le mot de passe de l'admin
try:
    admin = User.objects.get(username='admin')
    admin.set_password('AdminHopital2026!')
    admin.save()
    print("✅ Mot de passe de 'admin' réinitialisé avec succès!")
except User.DoesNotExist:
    # Si admin n'existe pas, le créer
    User.objects.create_superuser(
        username='admin',
        email='admin@hopital.com',
        password='AdminHopital2026!'
    )
    print("✅ Superutilisateur 'admin' créé avec succès!")
