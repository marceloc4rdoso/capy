# users/views.py
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import UserCreateForm, UserUpdateForm

SUCCESS_URL = reverse_lazy('user_list')

class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Usuários'
        return context


class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'form_template.html'
    success_url = SUCCESS_URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Novo Usuário'
        context['success_url'] = self.success_url
        return context

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'form_template.html'
    success_url = SUCCESS_URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Usuário'
        context['success_url'] = self.success_url
        return context

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'confirm_delete.html'
    success_url = SUCCESS_URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Confirmar Exclusão'
        context['message'] = f'Atenção! Excluir um usuário é uma ação irreversível. Deseja continuar e excluir {self.object.username}?'
        context['success_url'] = self.success_url
        return context