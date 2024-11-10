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