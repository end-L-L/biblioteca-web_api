from rest_framework import serializers
from django.contrib.auth.models import User
from biblioteca.models import Miembro

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