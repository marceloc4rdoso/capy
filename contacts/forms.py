# contacts/forms.py
from django import forms
from .models import Contact
from django.forms import inlineformset_factory
from .models import Address  # O Contact já deve estar importado
from pycpfcnpj import cpf, cnpj


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            "name",
            "email",
            "phone",
            "person_type",
            "organization_type",
            "logo",
            "document",
            "is_active",
            "company",
            "user",
        ]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "person_type": forms.Select(attrs={"class": "form-control"}),
            "document": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Apenas números"}
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "company": forms.Select(attrs={"class": "form-control"}),
            "user": forms.Select(attrs={"class": "form-control"}),
            "organization_type": forms.Select(attrs={"class": "form-control"}),
            "logo": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

        labels = {
            "name": "Nome / Razão Social",
            "email": "E-mail",
            "phone": "Telefone Principal",
            "person_type": "Tipo de Pessoa",
            "document": "CPF / CNPJ",
            "is_active": "Contato Ativo",
            "company": "Empresa Associada (PJ)",
            "user": "Usuário do Sistema Associado (Opcional)",
        }

        # Adicionar um pouco de validação e limpeza
        """
        def clean_document(self):
            document = self.cleaned_data.get("document", "")
            # Remove caracteres não numéricos
            return "".join(filter(str.isdigit, document))        
        
        """

        def clean(self):
            # Primeiro, execute a validação padrão do Django
            cleaned_data = super().clean()

            # Pegue os valores dos campos do dicionário cleaned_data
            person_type = cleaned_data.get("person_type")
            document = cleaned_data.get("document")

            # Se o campo de documento não foi preenchido, não há nada a validar
            if not document:
                return cleaned_data

            # A biblioteca pycpfcnpj já lida com documentos formatados (com pontos e traços),
            # então não precisamos limpar os caracteres manualmente.

            # Validação para Pessoa Jurídica (CNPJ)
            if person_type == Contact.PersonType.LEGAL:
                # A função cnpj.validate() retorna True se for válido, False caso contrário
                if not cnpj.validate(document):
                    # Se for inválido, adicione um erro ao campo 'document'
                    self.add_error("document", "O CNPJ informado é inválido.")

            # Validação para Pessoa Física (CPF)
            elif person_type == Contact.PersonType.INDIVIDUAL:
                # A função cpf.validate() retorna True se for válido, False caso contrário
                if not cpf.validate(document):
                    # Se for inválido, adicione um erro ao campo 'document'
                    self.add_error("document", "O CPF informado é inválido.")

            # É crucial retornar o cleaned_data no final
            return cleaned_data


# Cria o FormSet para os Endereços
AddressFormSet = inlineformset_factory(
    Contact,  # Modelo Pai
    Address,  # Modelo Filho
    fields=(
        "street",
        "number",
        "complement",
        "neighborhood",
        "city",
        "state",
        "zip_code",
    ),  # Campos a exibir
    extra=1,  # Quantos formulários em branco exibir por padrão
    can_delete=True,  # Adiciona um checkbox para marcar um endereço para exclusão
    widgets={
        "street": forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Logradouro"}
        ),
        "number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nº"}),
        "complement": forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Complemento"}
        ),
        "neighborhood": forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Bairro"}
        ),
        "city": forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Cidade"}
        ),
        "state": forms.TextInput(attrs={"class": "form-control", "placeholder": "UF"}),
        "zip_code": forms.TextInput(
            attrs={"class": "form-control", "placeholder": "CEP"}
        ),
    },
)
