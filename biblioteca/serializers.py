from rest_framework import serializers
from django.contrib.auth.models import User
from biblioteca.models import Miembro, AppSettings

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

class AppSettingsSerializer(serializers.ModelSerializer):
    dias_prestamo = serializers.IntegerField()
    cuota_mora = serializers.DecimalField(max_digits=5, decimal_places=2)
    cuota_extravio = serializers.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        model = AppSettings
        fields = ('dias_prestamo', 'cuota_mora', 'cuota_extravio')