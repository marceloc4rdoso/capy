from django.urls import path
from . import views
urlpatterns = [
    path('', views.contact_list, name='contact_list'),
    path('new/', views.contact_create, name='contact_create'),
    path('edit/<int:pk>/', views.contact_update, name='contact_update'),
    path('delete/<int:pk>/', views.contact_delete, name='contact_delete'),
]
# This file defines the URL patterns for the app_contacts application.
