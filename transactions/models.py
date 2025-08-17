# transactions/models.py
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from contacts.models import Contact
from inventory.models import Item


class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        SALE = "SALE", "Venda"  # Gera receita, diminui estoque
        PURCHASE = "PURCHASE", "Compra"  # Gera despesa, aumenta estoque

    transaction_type = models.CharField(
        max_length=10, choices=TransactionType.choices, verbose_name="Tipo de Transação"
    )
    contact = models.ForeignKey(
        Contact,
        on_delete=models.PROTECT,  # Proíbe deletar um contato que tem transações
        verbose_name="Contato (Cliente/Fornecedor)",
    )
    transaction_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Data da Transação"
    )
    total_value = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00, verbose_name="Valor Total"
    )
    notes = models.TextField(blank=True, null=True, verbose_name="Observações")

    def __str__(self):
        return f"{self.get_transaction_type_display()} #{self.pk} - {self.contact.name}"

    subtotal = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00, verbose_name="Subtotal"
    )
    discount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00, verbose_name="Desconto"
    )
    additions = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00, verbose_name="Acréscimos"
    )
    total_value = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00, verbose_name="Valor Total"
    )

    def update_totals(self):
        """Calcula o subtotal a partir dos itens e o total final."""
        subtotal_val = sum(item.total_price for item in self.items.all())
        self.subtotal = subtotal_val
        self.total_value = (self.subtotal - self.discount) + self.additions
        self.save(update_fields=["subtotal", "total_value"])

    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"
        ordering = ["-transaction_date"]


class TransactionItem(models.Model):
    transaction = models.ForeignKey(
        Transaction, related_name="items", on_delete=models.CASCADE
    )
    item = models.ForeignKey(Item, on_delete=models.PROTECT, verbose_name="Item")
    quantity = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Quantidade"
    )
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Preço Unitário"
    )

    @property
    def total_price(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"

    class Meta:
        verbose_name = "Item da Transação"
        verbose_name_plural = "Itens da Transação"


# --- Sinal para atualizar o estoque ---
# Usamos um "sinal" do Django para executar uma ação APÓS um item ser salvo.
# transactions/models.py


@receiver(post_save, sender=TransactionItem)
def update_stock_on_save(sender, instance, created, **kwargs):
    """
    Atualiza o estoque do item quando um TransactionItem é criado ou alterado.
    Também atualiza o valor total da transação.
    """
    item = instance.item
    transaction = instance.transaction

    if item.item_type == "PROD":
        total_purchased = sum(
            ti.quantity
            for ti in TransactionItem.objects.filter(
                item=item, transaction__transaction_type="PURCHASE"
            )
        )
        total_sold = sum(
            ti.quantity
            for ti in TransactionItem.objects.filter(
                item=item, transaction__transaction_type="SALE"
            )
        )
        item.stock_quantity = total_purchased - total_sold
        item.save(update_fields=["stock_quantity"])

    # Atualiza o valor total da transação pai
    # A verificação 'if created:' foi removida para garantir que o total seja
    # sempre atualizado, mesmo ao editar/remover itens.
    transaction.update_totals()  # <--- NOME DO MÉTODO CORRIGIDO
