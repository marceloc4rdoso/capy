# contacts/forms.py
from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'user']
        # O campo 'user' será renderizado como um dropdown com todos os usuários cadastrados,
        # o que é perfeito para associar um contato a um usuário existente.
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
        }
        
        labels = {
            'name': 'Nome Completo',
            'email': 'E-mail',
            'phone': 'Telefone',
            'user': 'Usuário Associado (Opcional)',
        }