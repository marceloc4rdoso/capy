# transactions/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Transaction, TransactionItem


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        # Adicionamos os campos de totais
        fields = ["contact", "notes", "discount", "additions"]
        widgets = {
            "contact": forms.Select(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "discount": forms.NumberInput(
                attrs={"class": "form-control total-field", "id": "discount"}
            ),
            "additions": forms.NumberInput(
                attrs={"class": "form-control total-field", "id": "additions"}
            ),
        }


# Formset para adicionar os itens na mesma página da transação
TransactionItemFormSet = inlineformset_factory(
    Transaction,
    TransactionItem,
    fields=("item", "quantity", "unit_price"),
    extra=1,  # Começa com um formulário em branco
    can_delete=True,
    widgets={
        "item": forms.Select(attrs={"class": "form-control"}),
        "quantity": forms.NumberInput(attrs={"class": "form-control"}),
        "unit_price": forms.NumberInput(attrs={"class": "form-control"}),
    },
)
