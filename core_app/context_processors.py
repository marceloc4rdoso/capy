# core_app/context_processors.py
from contacts.models import Contact
from django.core.cache import cache

def system_branding_processor(request):
    """
    Busca o contato principal (Gestor do Sistema) e disponibiliza 
    seu nome e logo para todos os templates, usando cache para eficiência.
    """
    # Chave para o cache, para não buscar no banco a cada requisição
    HOLDER_CACHE_KEY = 'system_holder_branding'
    
    # Tenta pegar os dados do cache
    holder_data = cache.get(HOLDER_CACHE_KEY)
    
    if not holder_data:
        # Se não estiver no cache, busca no banco de dados
        try:
            # Encontra o primeiro contato marcado como Gestor do Sistema
            system_holder = Contact.objects.get(
                organization_type=Contact.OrganizationType.SYSTEM_HOLDER
            )
            
            holder_data = {
                'system_holder_name': system_holder.name,
                'system_holder_logo': system_holder.logo,
            }
            
            # Guarda os dados no cache por 1 hora (3600 segundos) para otimizar
            cache.set(HOLDER_CACHE_KEY, holder_data, 3600)
            
        except Contact.DoesNotExist:
            # Se nenhum gestor for encontrado, define valores padrão
            holder_data = {
                'system_holder_name': 'CAPY GESTÃO',
                'system_holder_logo': None,
            }
        except Contact.MultipleObjectsReturned:
            # Se houver mais de um gestor, pega o primeiro (e talvez registre um aviso)
            system_holder = Contact.objects.filter(
                organization_type=Contact.OrganizationType.SYSTEM_HOLDER
            ).first()
            holder_data = {
                'system_holder_name': system_holder.name,
                'system_holder_logo': system_holder.logo,
            }
            cache.set(HOLDER_CACHE_KEY, holder_data, 3600)

    return holder_data