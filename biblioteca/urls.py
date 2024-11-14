from django.urls import path, include
from rest_framework import routers

from biblioteca.views import usuarios
from biblioteca.views import app
from biblioteca.views import biblioteca

routers = routers.DefaultRouter()

urlpatterns = [
    # Bibliotecarios y Miembros
    path("v1/create-admin", usuarios.BibliotecarioView.as_view(), name="create-admin"),
    path("v1/miembros", usuarios.MiembroView.as_view(), name="create-member"),

    # App
    path("v1/app-settings", app.SettingsView.as_view(), name="app-settings"),

    # Libros
    path("v1/editoriales", biblioteca.EditorialView.as_view(), name="editoriales"),
    path("v1/categorias", biblioteca.CategoriaView.as_view(), name="categorias"),
    path("v1/areas", biblioteca.AreaView.as_view(), name="areas"),
    path("v1/tipos", biblioteca.TipoEjemplarView.as_view(), name="tipos"),
    path("v1/estados", biblioteca.EstadoEjemplarView.as_view(), name="estados"),
    path("v1/libros", biblioteca.LibroView.as_view(), name="libros"),
    path("v1/ejemplares", biblioteca.EjemplarView.as_view(), name="ejemplares"),
    path("v1/prestamos", biblioteca.PrestamoView.as_view(), name="prestamos"),
    path("v1/devoluciones-response", biblioteca.DevolucionResponseView.as_view(), name="devoluciones-response"),
    path("v1/devoluciones", biblioteca.DevolucionView.as_view(), name="devoluciones"),
    path("v1/lista-prestamos", biblioteca.ListaPrestamosView.as_view(), name="lista-prestamos")
]