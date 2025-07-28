# transactions/views.py
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transaction, Contact
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .forms import TransactionForm, TransactionItemFormSet

class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'
    
    def get_queryset(self):
        # Filtra as transações com base no tipo vindo da URL (compras ou vendas)
        return Transaction.objects.filter(
            transaction_type=self.kwargs['transaction_type'].upper()
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Passa o tipo para o template para sabermos o título e os links corretos
        ttype = self.kwargs['transaction_type']
        context['transaction_type'] = ttype
        context['title'] = 'Vendas' if ttype == 'vendas' else 'Compras'
        return context


# NOVA VIEW: ContactSelectionView
class ContactSelectionView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = 'transactions/contact_selection.html'
    context_object_name = 'contacts'

    def get_queryset(self):
        queryset = Contact.objects.filter(is_active=True)
        # Lógica de busca simples
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(document__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ttype = self.kwargs['transaction_type']
        context['transaction_type'] = ttype
        context['title'] = f"Selecionar {'Cliente' if ttype == 'vendas' else 'Fornecedor'}"
        return context


# VIEW MODIFICADA: TransactionCreateView
class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'

    def get_success_url(self):
        ttype = self.kwargs['transaction_type']
        return reverse_lazy('transaction_list', kwargs={'transaction_type': ttype})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ttype = self.kwargs['transaction_type']
        contact_pk = self.kwargs['contact_pk']
        
        # Carrega os dados do contato selecionado
        contact = get_object_or_404(Contact, pk=contact_pk)
        context['contact'] = contact
        
        context['transaction_type'] = ttype
        context['title'] = 'Nova Venda' if ttype == 'vendas' else 'Nova Compra'
        
        if self.request.POST:
            context['formset'] = TransactionItemFormSet(self.request.POST, prefix='items')
        else:
            context['formset'] = TransactionItemFormSet(prefix='items')
        return context

    def form_valid(self, form):
        ttype = self.kwargs['transaction_type'].upper()
        contact_pk = self.kwargs['contact_pk']
        
        # Associa o tipo e o contato à transação
        form.instance.transaction_type = ttype
        form.instance.contact = get_object_or_404(Contact, pk=contact_pk)
        
        context = self.get_context_data()
        formset = context['formset']
        
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            
            # Atualiza os totais após salvar os itens
            self.object.update_totals()
            
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    # Sobrescreve o get_form para remover o campo 'contact', pois já o temos
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields.pop('contact', None)
        return form

# VIEW MODIFICADA: TransactionDetailView
class TransactionDetailView(LoginRequiredMixin, DetailView):
    model = Transaction
    template_name = 'transactions/transaction_detail.html'
    context_object_name = 'transaction'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalhes da Transação'
        return context
# VIEW MODIFICADA: TransactionUpdateView
class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Transação'
        return context  