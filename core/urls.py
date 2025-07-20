# core/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), # Sistema de login/logout do Django

     # URLs dos apps de CRUD
    path('users/', include('users.urls')),
    path('contacts/', include('contacts.urls')),
    #path('purchases/', include('purchases.urls')),
    #path('sales/', include('sales.urls')),

    # URL principal (deve vir por último para não capturar as outras)
    path('', include('core_app.urls')), # Nossas URLs principais (home, dashboard)
]