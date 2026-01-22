#!/usr/bin/env python
"""
Script pour créer un superutilisateur automatiquement au déploiement sur Render.
À exécuter une seule fois après le premier déploiement.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Vérifier si le superutilisateur existe déjà
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@hopital.com',
        password='AdminHopital2026!'  # CHANGEZ CE MOT DE PASSE !
    )
    print("✅ Superutilisateur 'admin' créé avec succès!")
else:
    print("ℹ️ Le superutilisateur 'admin' existe déjà.")
