# contacts/models.py
from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
    # O user associado a este contato.
    # on_delete=models.SET_NULL: Se o usuário for deletado, o contato permanece, mas o campo 'user' fica nulo.
    # null=True: Permite que o campo seja nulo no banco de dados.
    # blank=True: Permite que o campo seja vazio em formulários.
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    name = models.CharField(max_length=255, verbose_name="Nome Completo")
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Contato"
        verbose_name_plural = "Contatos"