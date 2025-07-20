# contacts/urls.py
from django.urls import path
from .views import ContactCreateView, ContactUpdateView, ContactDeleteView

urlpatterns = [
    path('create/', ContactCreateView.as_view(), name='contact_create'),
    path('<int:pk>/update/', ContactUpdateView.as_view(), name='contact_update'),
    path('<int:pk>/delete/', ContactDeleteView.as_view(), name='contact_delete'),
]