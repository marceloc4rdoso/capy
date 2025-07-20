# core_app/views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import User
from contacts.models import Contact

# View para a página inicial (pública)
class HomeView(TemplateView):
    template_name = 'home.html'

# View para o dashboard (requer login)
# LoginRequiredMixin cuida da segurança, redirecionando para a página de login se o usuário não estiver logado.
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

class ManagementListView(LoginRequiredMixin, TemplateView):
    template_name = 'management_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # .select_related('user') otimiza a consulta, evitando múltiplos acessos ao banco
        # para buscar o usuário de cada contato.
        context['contacts'] = Contact.objects.all().select_related('user')
        context['users'] = User.objects.all()
        context['title'] = 'Gestão de Usuários e Contatos'
        return context