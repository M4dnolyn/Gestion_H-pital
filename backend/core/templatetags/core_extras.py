from django import template

register = template.Library()

@register.filter(name='has_role')
def has_role(user, roles_string):
    """
    Vérifie si l'utilisateur a l'un des rôles spécifiés.
    Usage: {% if user|has_role:"ADMIN,DIR" %}
    """
    if user.is_superuser:
        return True
    
    if not hasattr(user, 'personnel_profile'):
        return False
        
    roles = [role.strip() for role in roles_string.split(',')]
    personnel = getattr(user, 'personnel_profile', None)
    if not personnel:
        return False
    return personnel.fonction in roles

@register.filter(name='mul')
def mul(value, arg):
    """Multiplie la valeur par l'argument"""
    try:
        return value * arg
    except (ValueError, TypeError):
        return 0
