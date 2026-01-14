# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from personnes.models import Personnel

class User(AbstractUser):
    personnel = models.OneToOneField(
        Personnel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='compte_utilisateur'
    )
    
    # Ajoutez ces related_name pour éviter les conflits
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='accounts_user_set',  # CHANGEMENT ICI
        related_query_name='accounts_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='accounts_user_set',  # CHANGEMENT ICI
        related_query_name='accounts_user',
    )
    
    def get_role(self):
        if self.personnel:
            return self.personnel.fonction
        return None
    
    def __str__(self):
        return self.username
