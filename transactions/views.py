# transactions/views.py
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transaction
from .forms import TransactionForm, TransactionItemFormSet


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "transactions/transaction_list.html"
    context_object_name = "transactions"

    # Este método é a chave para reutilizar a view
    def get_queryset(self):
        # Filtra as transações com base no tipo vindo da URL (compra ou venda)
        return Transaction.objects.filter(
            transaction_type=self.kwargs["transaction_type"].upper()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Passa o tipo para o template para sabermos o título e os links corretos
        ttype = self.kwargs["transaction_type"]
        context["transaction_type"] = ttype
        context["title"] = "Vendas" if ttype == "vendas" else "Compras"
        return context


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "transactions/transaction_form.html"

    def get_success_url(self):
        ttype = self.kwargs["transaction_type"]
        return reverse_lazy("transaction_list", kwargs={"transaction_type": ttype})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ttype = self.kwargs["transaction_type"]
        context["transaction_type"] = ttype
        context["title"] = "Nova Venda" if ttype == "vendas" else "Nova Compra"
        if self.request.POST:
            context["formset"] = TransactionItemFormSet(self.request.POST)
        else:
            context["formset"] = TransactionItemFormSet()
        return context

    def form_valid(self, form):
        # Define o tipo da transação antes de salvar
        ttype = self.kwargs["transaction_type"].upper()
        form.instance.transaction_type = ttype

        context = self.get_context_data()
        formset = context["formset"]

        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            # O sinal 'post_save' cuidará de atualizar o estoque e o valor total
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))
