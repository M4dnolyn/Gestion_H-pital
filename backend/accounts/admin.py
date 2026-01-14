from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'personnel', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'personnel__fonction')
    search_fields = ('username', 'email', 'personnel__nom', 'personnel__prenom')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('email', 'personnel')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'personnel', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
