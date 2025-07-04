from django import forms
from django.contrib.auth.forms import UserCreationForm
from applications.security.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'dni', 'phone', 'direction', 'image',
            'is_active', 'is_staff', 'is_superuser'
        ]
        widgets = {
            'icon': forms.TextInput(attrs={'placeholder': 'fa-solid fa-user'}),
            'order': forms.NumberInput(attrs={'min': 0}),
            'dni': forms.TextInput(attrs={'placeholder': 'Cédula o RUC'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Teléfono'}),
            'direction': forms.TextInput(attrs={'placeholder': 'Dirección'}),
            'image': forms.ClearableFileInput(),
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'dni', 'phone', 'direction', 'image',
            'password1', 'password2'
        ]
        widgets = {
            'direction': forms.TextInput(attrs={'placeholder': 'Dirección'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Teléfono'}),
            'dni': forms.TextInput(attrs={'placeholder': 'Cédula o RUC'}),
        }