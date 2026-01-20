#!/usr/bin/env bash
set -o errexit

# Installer les dépendances
pip install -r requirements.txt

# Aller dans backend
cd backend

# Créer le dossier static s'il n'existe pas
mkdir -p static

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Appliquer les migrations
python manage.py migrate
