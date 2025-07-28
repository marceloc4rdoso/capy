# transactions/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Transaction, TransactionItem

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['contact', 'notes']
        widgets = {
            'contact': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# Formset para adicionar os itens na mesma página da transação
TransactionItemFormSet = inlineformset_factory(
    Transaction,
    TransactionItem,
    fields=('item', 'quantity', 'unit_price'),
    extra=1, # Começa com um formulário em branco
    can_delete=True,
    widgets={
        'item': forms.Select(attrs={'class': 'form-control'}),
        'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        'unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
    }
)