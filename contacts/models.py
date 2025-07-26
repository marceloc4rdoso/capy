# contacts/models.py
from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
    class PersonType(models.TextChoices):
        INDIVIDUAL = 'PF', 'Pessoa Física'
        LEGAL = 'PJ', 'Pessoa Jurídica'

    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    name = models.CharField(max_length=255, verbose_name="Nome Completo")
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")

        # --- Campos de Identificação e Tipo ---
    person_type = models.CharField(
        max_length=2,
        choices=PersonType.choices,
        default=PersonType.INDIVIDUAL,
        verbose_name="Tipo de Pessoa"
    )
    document = models.CharField(max_length=18, unique=True, blank=True, null=True, verbose_name="CPF/CNPJ")
    
    # --- Status e Associações ---
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Usuário Associado")
    
    # --- Relação entre Contatos (PJ -> PF) ---
    # Um contato (PF) pode pertencer a uma empresa (PJ)
    # related_name='associated_contacts' permite que, a partir de um contato PJ,
    # possamos acessar contact.associated_contacts.all() para ver os PFs ligados a ele.
    company = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Empresa Associada (PJ)",
        limit_choices_to={'person_type': 'PJ'} # Garante que só PJs possam ser selecionadas aqui
    )
    
    # --- Timestamps ---
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Contato"
        verbose_name_plural = "Contatos"
        ordering = ['name']

    


    class OrganizationType(models.TextChoices):
        SYSTEM_HOLDER = 'HOLDER', 'Gestor do Sistema' # A sua empresa
        CLIENT = 'CLIENT', 'Cliente'                 # As empresas clientes
        OTHER = 'OTHER', 'Outro'                     # Outros tipos de contato PJ
        
        
    organization_type = models.CharField(
        max_length=10,
        choices=OrganizationType.choices,
        default=OrganizationType.OTHER,
        verbose_name="Classificação da Organização",
        blank=True,
    )
    
    # NOVO CAMPO PARA LOGOMARCA
    # upload_to='logos/' cria uma subpasta 'logos' dentro da sua pasta 'media'
    logo = models.ImageField(
        upload_to='logos/', 
        null=True, 
        blank=True, 
        verbose_name="Logomarca da Empresa"
    )

class Address(models.Model):
    contact = models.ForeignKey('Contact', related_name='addresses', on_delete=models.CASCADE)
    type_address = models.CharField(
        max_length=50, 
        choices=[
            ('residential', 'Residencial'),
            ('commercial', 'Comercial'),
            ('billing', 'Cobrança'),
            ('shipping', 'Entrega')
        ],
        default='Comercial',
        verbose_name="Tipo de Endereço"
    )
    street = models.CharField(max_length=255, verbose_name="Logradouro")
    number = models.CharField(max_length=20, verbose_name="Número")
    complement = models.CharField(max_length=100, blank=True, null=True, verbose_name="Complemento")
    neighborhood = models.CharField(max_length=100, verbose_name="Bairro")
    city = models.CharField(max_length=100, verbose_name="Cidade")
    state = models.CharField(max_length=2, verbose_name="UF") # Sigla do estado, ex: SP
    zip_code = models.CharField(max_length=9, verbose_name="CEP") # Formato 12345-678
    country = models.CharField(max_length=50, default='Brasil', verbose_name="País")

    def __str__(self):
        return f"{self.street}, {self.number} - {self.city}"

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"
        ordering = ['type_address', 'city', 'neighborhood']

