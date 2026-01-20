from django import forms
from django.contrib.auth import get_user_model
from personnes.models import Personnel

User = get_user_model()

class UserCreationForm(forms.ModelForm):
    """Formulaire pour la création d'un utilisateur lié à un membre du personnel"""
    
    personnel = forms.ModelChoiceField(
        queryset=Personnel.objects.filter(user__isnull=True),
        label="Membre du personnel",
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Sélectionnez un membre du personnel qui n'a pas encore de compte utilisateur."
    )
    
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8
    )
    
    password_confirm = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Les mots de passe ne correspondent pas.")
            
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            # Lier le personnel à l'utilisateur
            personnel = self.cleaned_data["personnel"]
            personnel.user = user
            personnel.save()
        return user
