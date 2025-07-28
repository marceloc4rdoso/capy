# core/urls.py
from django.contrib import admin
from django.urls import path, include

# ADICIONE ESTES IMPORTS
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "accounts/", include("django.contrib.auth.urls")
    ),  # Sistema de login/logout do Django
    # URLs dos apps de CRUD
    path("users/", include("users.urls")),
    path("contacts/", include("contacts.urls")),
    # path('purchases/', include('purchases.urls')),
    # path('sales/', include('sales.urls')),
    # URL principal (deve vir por último para não capturar as outras)
    path("", include("core_app.urls")),  # Nossas URLs principais (home, dashboard)
    # Deixamos um path vazio para capturar /compras e /vendas
    path('', include('transactions.urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
