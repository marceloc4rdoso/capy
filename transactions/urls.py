# transactions/urls.py
from django.urls import path
from .views import TransactionListView, TransactionCreateView, ContactSelectionView

urlpatterns = [
    # A URL captura se é 'compras' ou 'vendas' e passa para a view
    path(
        "<str:transaction_type>/",
        TransactionListView.as_view(),
        name="transaction_list",
    ),
    # Nova rota para a tela de seleção
    path(
        "<str:transaction_type>/selecionar-contato/",
        ContactSelectionView.as_view(),
        name="contact_selection",
    ),
    # A rota de criação agora espera um ID de contato
    path(
        "<str:transaction_type>/<int:contact_pk>/nova/",
        TransactionCreateView.as_view(),
        name="transaction_create",
    ),
]
