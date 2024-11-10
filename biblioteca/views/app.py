from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from biblioteca.models import AppSettings

from biblioteca.serializers import AppSettingsSerializer

class SettingsView(APIView):

    def post(self, request):
        # Obtiene la configuración actual, o crea una nueva si no existe
        app_settings, created = AppSettings.objects.get_or_create(id=1)
        
        # Serializa los datos para la actualización parcial
        serializer = AppSettingsSerializer(app_settings, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()  # Guarda solo los datos enviados en la solicitud
            return Response({"mensaje": "Ajustes actualizados"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        