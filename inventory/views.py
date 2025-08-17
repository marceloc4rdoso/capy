from django.shortcuts import render

# inventory/views.py
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Item
from .forms import ItemForm

SUCCESS_URL = reverse_lazy("item_list")


class ItemListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = "inventory/item_list.html"
    context_object_name = "items"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Produtos e Serviços"
        return context


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    template_name = "inventory/item_form.html"
    success_url = SUCCESS_URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Novo Item"
        return context


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    form_class = ItemForm
    template_name = "inventory/item_form.html"
    success_url = SUCCESS_URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Editar Item"
        return context


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = "confirm_delete.html"  # Reutilizando o template global
    success_url = SUCCESS_URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Confirmar Exclusão"
        context["message"] = (
            f"Você tem certeza que deseja excluir o item: {self.object.name}?"
        )
        return context
