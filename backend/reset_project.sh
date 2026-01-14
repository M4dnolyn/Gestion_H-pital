#!/bin/bash
echo "1. Nettoyage des migrations..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

echo "2. Reset de la base PostgreSQL..."
sudo -u postgres psql << PSQL_EOF
DROP DATABASE IF EXISTS gestion_hopital;
CREATE DATABASE gestion_hopital OWNER hopital_user;
\c gestion_hopital
GRANT ALL ON SCHEMA public TO hopital_user;
GRANT CREATE ON SCHEMA public TO hopital_user;
PSQL_EOF

echo "3. Création des migrations..."
python manage.py makemigrations

echo "4. Application des migrations..."
python manage.py migrate

echo "5. Création du superuser..."
python manage.py createsuperuser

echo "6. Test du serveur..."
python manage.py runserver
