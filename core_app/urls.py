# core_app/urls.py
from django.urls import path
from .views import HomeView, DashboardView, ManagementListView

urlpatterns = [
    # O nome 'home' e 'dashboard' será usado no redirect e nos templates
    path("", HomeView.as_view(), name="home"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("management/", ManagementListView.as_view(), name="management_list"),
]
