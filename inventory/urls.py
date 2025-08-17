# inventory/urls.py
from django.urls import path
from .views import ItemListView, ItemCreateView, ItemUpdateView, ItemDeleteView

urlpatterns = [
    path("", ItemListView.as_view(), name="item_list"),
    path("novo/", ItemCreateView.as_view(), name="item_create"),
    path("<int:pk>/editar/", ItemUpdateView.as_view(), name="item_update"),
    path("<int:pk>/excluir/", ItemDeleteView.as_view(), name="item_delete"),
]
