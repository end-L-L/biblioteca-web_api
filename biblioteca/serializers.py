from rest_framework import serializers
from django.contrib.auth.models import User
from biblioteca.models import *

# Usuarios

class UserSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')

class MiembroSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    matricula = serializers.IntegerField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    is_active = serializers.BooleanField(required=False)

    class Meta:
        model = Miembro
        fields = ('id', 'matricula', 'first_name', 'last_name', 'is_active')

# App

class AppSettingsSerializer(serializers.ModelSerializer):
    dias_prestamo = serializers.IntegerField()
    cuota_mora = serializers.DecimalField(max_digits=5, decimal_places=2)
    cuota_extravio = serializers.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        model = AppSettings
        fields = ('dias_prestamo', 'cuota_mora', 'cuota_extravio')

# Biblioteca

class EditorialSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(required=True)

    class Meta:
        model = Editorial
        fields = ('id', 'nombre')

class CategoriaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(required=True)

    class Meta:
        model = Categoria
        fields = ('id', 'nombre')

class AreaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(required=True)

    class Meta:
        model = Area
        fields = ('id', 'nombre')

class TipoEjemplarSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    tipo = serializers.CharField(required=True)

    class Meta:
        model = Tipo_Ejemplar
        fields = ('id', 'tipo')

class EstadoEjemplarSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    estado = serializers.CharField(required=True)

    class Meta:
        model = Estado_Ejemplar
        fields = ('id', 'estado')

class LibroSerializer(serializers.ModelSerializer):
    isbn = serializers.CharField(required=True)
    titulo = serializers.CharField(required=True)
    fecha_de_publicacion = serializers.DateField()
    edicion = serializers.CharField(required=True)
    editorial = serializers.PrimaryKeyRelatedField(queryset=Editorial.objects.all())
    categoria = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all())
    area = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all())

    class Meta:
        model = Libro
        fields = ('isbn', 'titulo', 'autor', 'editorial', 'fecha_de_publicacion', 'edicion', 'categoria', 'area')

class EjemplarSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    isbn = serializers.PrimaryKeyRelatedField(queryset=Libro.objects.all())
    #estado = serializers.CharField(required=True)
    estado = serializers.PrimaryKeyRelatedField(queryset=Estado_Ejemplar.objects.all())
    tipo = serializers.PrimaryKeyRelatedField(queryset=Tipo_Ejemplar.objects.all())
    disponible = serializers.BooleanField(required=False)

    class Meta:
        model = Ejemplar
        fields = ('id', 'isbn', 'estado', 'tipo', 'disponible')

class PrestamoSerializer(serializers.ModelSerializer):
        
    ejemplar_id = serializers.PrimaryKeyRelatedField(queryset=Ejemplar.objects.all())
    miembro_id = serializers.PrimaryKeyRelatedField(queryset=Miembro.objects.all())
    fecha_inicio = serializers.DateField(required=True)
    fecha_fin = serializers.DateField(required=True)
    estado_libro = serializers.IntegerField(required=True)
    estado_prestamo = serializers.BooleanField(required=False)
    recargo = serializers.BooleanField(required=False)
    fecha_devolucion = serializers.DateField(required=False)
    recargo = serializers.BooleanField()

    class Meta:
        model = Prestamo
        fields = ('ejemplar_id', 'miembro_id', 'fecha_inicio', 'fecha_fin', 'estado_libro' ,'estado_prestamo', 'fecha_devolucion', 'recargo')

class PrestamoDataSerializer(serializers.ModelSerializer):
    isbn = serializers.CharField(required=True)
    miembro_id = serializers.IntegerField(required=True)
    fecha_inicio = serializers.DateField(required=True)
    fecha_fin = serializers.DateField(required=True)
    #estado_libro = serializers.IntegerField(required=True)

    class Meta:
        model = Prestamo
        fields = ('isbn', 'miembro_id', 'fecha_inicio', 'fecha_fin')

