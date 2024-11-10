from django.urls import path, include
from rest_framework import routers
from biblioteca.views import usuarios
from biblioteca.views import app

routers = routers.DefaultRouter()

urlpatterns = [
    # Bibliotecarios y Miembros
    path("v1/create-admin", usuarios.BibliotecarioView.as_view(), name="create-admin"),
    path("v1/create-member", usuarios.MiembroView.as_view(), name="create-member"),

    # App
    path("v1/app-settings", app.SettingsView.as_view(), name="app-settings")
]