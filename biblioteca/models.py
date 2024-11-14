from django.db import models
from django.contrib.auth.models import User

# Usuarios 

class Bibliotecario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.user.email}"

class Miembro(models.Model):
    matricula = models.IntegerField()
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} - Matrícula: {self.matricula}"
    
# App

class AppSettings(models.Model):
    dias_prestamo = models.IntegerField(default=3)
    cuota_mora = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    cuota_extravio = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

# Libros

class Editorial(models.Model):
    nombre = models.CharField(max_length=128)

class Categoria(models.Model):
    nombre = models.CharField(max_length=128)

class Area(models.Model):
    nombre = models.CharField(max_length=128)

class Tipo_Ejemplar(models.Model):
    tipo = models.CharField(max_length=32)

class Estado_Ejemplar(models.Model):
    estado = models.CharField(max_length=32)

class Libro(models.Model):
    isbn = models.CharField(max_length=32, primary_key=True)
    titulo = models.CharField(max_length=128)
    autor = models.CharField(max_length=256)
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)
    fecha_de_publicacion = models.DateField()
    edicion = models.CharField(max_length=32)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)

class Ejemplar(models.Model):
    isbn = models.ForeignKey(Libro, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado_Ejemplar, on_delete=models.CASCADE)
    tipo = models.ForeignKey(Tipo_Ejemplar, on_delete=models.CASCADE)
    disponible = models.BooleanField(default=True)

class Prestamo(models.Model):
    miembro = models.ForeignKey(Miembro, on_delete=models.CASCADE)
    ejemplar = models.ForeignKey(Ejemplar, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado_libro = models.IntegerField(null=True)
    estado_prestamo = models.BooleanField(default=False)
    recargo = models.BooleanField(default=False)
    fecha_devolucion = models.DateField(null=True)