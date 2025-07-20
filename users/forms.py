# users/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Usamos UserCreationForm como base para criar usuários, pois ele lida com a senha de forma segura.
class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

# Para editar, criamos um ModelForm normal, sem o campo de senha.
# A alteração de senha deve ser um processo separado e mais seguro.
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_active', 'is_staff']

        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'is_active': 'Ativo',
            'is_staff': 'Acesso ao Admin',
        }