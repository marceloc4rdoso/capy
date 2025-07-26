# contacts/views.py
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Contact
from .forms import ContactForm, AddressFormSet

# O 'management_list' é o nome da URL que criaremos para a lista unificada.
SUCCESS_URL = reverse_lazy("contact_list")


class ContactListView(LoginRequiredMixin, ListView):
    model = Contact
    # É uma boa prática colocar templates específicos do app em um subdiretório
    template_name = "contacts/contact_list.html"
    context_object_name = "contacts"  # Define o nome da variável no template
    paginate_by = 15  # Opcional: Adiciona paginação para listas grandes

    def get_queryset(self):
        # Pega o parâmetro 'status' da URL, ex: /contacts/?status=inactive
        status = self.request.GET.get("status")
        if status == "inactive":
            # Se o status for 'inactive', retorna os contatos inativos
            return Contact.objects.filter(is_active=False).select_related(
                "company", "user"
            )
        # Por padrão, ou se 'status' não for 'inactive', retorna os ativos
        return Contact.objects.filter(is_active=True).select_related("company", "user")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_status"] = self.request.GET.get("status", "active")
        context["title"] = "Lista de Contatos"
        return context


class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "form_template.html"
    success_url = SUCCESS_URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Novo Contato"
        context["success_url"] = self.success_url
        return context


class ContactUpdateView(LoginRequiredMixin, UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = "contacts/contact_form_with_addresses.html"
    # success_url = SUCCESS_URL
    success_url = reverse_lazy("contact_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Editar Contato"
        # context['success_url'] = self.success_url
        if self.request.POST:
            context["address_formset"] = AddressFormSet(
                self.request.POST, instance=self.object
            )
        else:
            context["address_formset"] = AddressFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        address_formset = context["address_formset"]

        if address_formset.is_valid():
            self.object = form.save()
            address_formset.instance = self.object
            address_formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = "confirm_delete.html"
    success_url = SUCCESS_URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Confirmar Exclusão"
        context["message"] = (
            f"Você tem certeza que deseja excluir o contato: {self.object.name}?"
        )
        context["success_url"] = self.success_url
        return context


class ContactDetailView(LoginRequiredMixin, DetailView):
    model = Contact
    template_name = "contacts/contact_detail.html"
    context_object_name = "contact"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # O objeto 'contact' já está no contexto, podemos usá-lo com self.object
        contact = self.get_object()

        # Buscamos os endereços relacionados a este contato
        context["addresses"] = contact.addresses.all()

        # Se for uma Pessoa Jurídica, buscamos os contatos associados a ela
        if contact.person_type == "PJ":
            context["associated_contacts"] = Contact.objects.filter(company=contact)

        context["title"] = f"Detalhes de {contact.name}"
        return context
