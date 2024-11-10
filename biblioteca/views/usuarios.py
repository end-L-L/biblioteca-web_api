from django.contrib.auth.models  import User

from biblioteca.serializers import UserSerializer
from biblioteca.serializers import MiembroSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from biblioteca.models import Bibliotecario
from biblioteca.models import Miembro

class BibliotecarioView(APIView):

    def post(self, request):
        user = UserSerializer(data=request.data)
        if user.is_valid():
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            email = request.data['email']
            username = request.data['email']
            password = request.data['password']

            # validar email
            if User.objects.filter(email=email).exists():
                return Response({"message": "email ya registrado"}, 400)
        
            # crear usuario - bibliotecario
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                is_active=1
            )

            # password encriptada
            user.set_password(password)
            user.save()

            bibliotecario = Bibliotecario.objects.create(user=user)

            bibliotecario.save()

            return Response({"id_bibliotecario_creado ": bibliotecario.id}, 201)
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)

class MiembroView(APIView):

    def post(self, request):
        user_serializer = MiembroSerializer(data=request.data)
        if user_serializer.is_valid():
            matricula = user_serializer.validated_data['matricula']

            # validar si la matrícula ya existe
            if Miembro.objects.filter(matricula=matricula).exists():
                return Response({"message": "matricula ya registrada"}, status=status.HTTP_400_BAD_REQUEST)

            # crear miembro usando el serializador
            miembro = user_serializer.save()

            return Response({"id_miembro_creado": miembro.id}, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
