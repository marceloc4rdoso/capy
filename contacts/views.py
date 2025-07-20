# contacts/views.py
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Contact
from .forms import ContactForm

# O 'management_list' é o nome da URL que criaremos para a lista unificada.
SUCCESS_URL = reverse_lazy('management_list')

class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'form_template.html'
    success_url = SUCCESS_URL
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Novo Contato'
        return context

class ContactUpdateView(LoginRequiredMixin, UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = 'form_template.html'
    success_url = SUCCESS_URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Contato'
        return context

class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = 'confirm_delete.html'
    success_url = SUCCESS_URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Confirmar Exclusão'
        context['message'] = f'Você tem certeza que deseja excluir o contato: {self.object.name}?'
        return context