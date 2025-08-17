# inventory/forms.py
from django import forms
from .models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["name", "description", "item_type", "stock_quantity", "is_active"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "item_type": forms.Select(attrs={"class": "form-control"}),
            "stock_quantity": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Apenas para produtos"}
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

        labels = {
            "name": "Nome do Item",
            "description": "Descrição",
            "item_type": "Tipo de Item",
            "stock_quantity": "Quantidade em Estoque Inicial",
            "is_active": "Item Ativo",
        }
