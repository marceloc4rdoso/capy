# transactions/urls.py
from django.urls import path
from .views import TransactionListView, TransactionCreateView

urlpatterns = [
    # A URL captura se é 'compras' ou 'vendas' e passa para a view
    path(
        "<str:transaction_type>/",
        TransactionListView.as_view(),
        name="transaction_list",
    ),
    path(
        "<str:transaction_type>/nova/",
        TransactionCreateView.as_view(),
        name="transaction_create",
    ),
]
