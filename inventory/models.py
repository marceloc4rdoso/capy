# inventory/models.py
from django.db import models


class Item(models.Model):
    class ItemType(models.TextChoices):
        PRODUCT = "PROD", "Produto"
        SERVICE = "SERV", "Serviço"

    name = models.CharField(max_length=255, verbose_name="Nome do Item")
    description = models.TextField(blank=True, null=True, verbose_name="Descrição")
    item_type = models.CharField(
        max_length=4,
        choices=ItemType.choices,
        default=ItemType.PRODUCT,
        verbose_name="Tipo de Item",
    )

    # Campo de estoque. Para serviços, pode ser ignorado ou usado para controlar "horas disponíveis".
    stock_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Quantidade em Estoque",
    )

    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Item (Produto/Serviço)"
        verbose_name_plural = "Itens (Produtos/Serviços)"
        ordering = ["name"]
