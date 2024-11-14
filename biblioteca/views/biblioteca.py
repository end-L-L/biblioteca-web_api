import datetime
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from biblioteca.models import *
from biblioteca.serializers import *

class EditorialView(APIView):
    
    def get(self, request):
        editoriales = Editorial.objects.all()
        serializer = EditorialSerializer(editoriales, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EditorialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CategoriaView(APIView):
    
    def get(self, request):
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AreaView(APIView):
    
    def get(self, request):
        areas = Area.objects.all()
        serializer = AreaSerializer(areas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AreaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TipoEjemplarView(APIView):
        
    def get(self, request):
        tipos = Tipo_Ejemplar.objects.all()
        serializer = TipoEjemplarSerializer(tipos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TipoEjemplarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EstadoEjemplarView(APIView):   
    def get(self, request):
        estados = Estado_Ejemplar.objects.all()
        serializer = EstadoEjemplarSerializer(estados, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EstadoEjemplarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LibroView(APIView):
        
    def get(self, request):
        libros = Libro.objects.all()
        serializer = LibroSerializer(libros, many=True)
        return Response(serializer.data)

    def post(self, request):
        
        serializer = LibroSerializer(data=request.data)
        if serializer.is_valid():
            
            duplicate_isbn = Libro.objects.filter(isbn=request.data['isbn'])
        
            if duplicate_isbn:
                return Response({"message":"isbn "+request.data.get('isbn')+", is already taken"},400)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EjemplarView(APIView):

    def get(self, request):
        ejemplares = Ejemplar.objects.all()
        serializer = EjemplarSerializer(ejemplares, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EjemplarSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PrestamoView(APIView):

    def get(self, request):
        prestamos = Prestamo.objects.all()
        serializer = PrestamoSerializer(prestamos, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = PrestamoDataSerializer(data=request.data)

        if serializer.is_valid():
            isbn = request.data.get("isbn")
            miembro_id = request.data.get("miembro_id")
            fecha_inicio = request.data.get("fecha_inicio")
            fecha_fin = request.data.get("fecha_fin")
            #estado = request.data.get("estado_libro")

            # Buscar un ejemplar disponible con el ISBN dado
            try:
                ejemplar = Ejemplar.objects.filter(isbn__isbn=isbn, disponible=True).first()
                if not ejemplar:
                    return Response({"error": "No hay ejemplares disponibles con este ISBN"}, status=status.HTTP_404_NOT_FOUND)
                
                # Crear el préstamo
                #miembro = Miembro.objects.get(id=miembro_id)
                miembro = Miembro.objects.filter(id=miembro_id, is_active=True).first()
                if not miembro:
                    return Response({"error": "Miembro Encontrado, Pero no Activo"}, status=status.HTTP_404_NOT_FOUND)
                
                # Comprobar si el miembro tiene menos de 3 préstamos activos
                if miembro.prestamo_set.filter(estado_prestamo=True).count() >= 3:
                    return Response({"error": "El miembro ya tiene 3 préstamos activos"}, status=status.HTTP_400_BAD_REQUEST)
                
                # Comprobar que el miembro no tenga préstamos vencidos
                if miembro.prestamo_set.filter(fecha_fin__lt=datetime.date.today(), estado_prestamo=True).count() > 0:
                    return Response({"error": "El miembro tiene préstamos vencidos"}, status=status.HTTP_400_BAD_REQUEST)
            
                # comprobar que el miembro no tenga un prestamo con el mismo isbn
                if miembro.prestamo_set.filter(ejemplar__isbn__isbn=isbn, estado_prestamo=True).count() > 0:
                    return Response({"error": "El miembro ya tiene un préstamo con este ISBN"}, status=status.HTTP_400_BAD_REQUEST)

                # seleccionar ejemplar que no este deteriorado (diferente de id 2)
                # if ejemplar.estado.id == 2:
                #     return Response({"error": "El ejemplar esta deteriorado"}, status=status.HTTP_400_BAD_REQUEST)
                            
                prestamo = Prestamo.objects.create(
                    miembro=miembro,
                    ejemplar=ejemplar,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                    #estado_libro=estado,
                    estado_prestamo=True
                )
                
                # Marcar el ejemplar como no disponible
                ejemplar.disponible = False
                ejemplar.save()
                
                return Response({"mensaje": "Préstamo creado exitosamente", "prestamo_id": prestamo.id}, status=status.HTTP_201_CREATED)
            
            except Miembro.DoesNotExist:
                return Response({"error": "Miembro no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DevolucionResponseView(APIView):
    def post(self, request):
        isbn = request.data.get("isbn")
        id_miembro = request.data.get("id_miembro")
        id_estado = request.data.get("id_estado")

        print(isbn)
        print(id_miembro)
        print(id_estado)

        miembro = Miembro.objects.filter(id=id_miembro, is_active=True).first()
        prestamo = Prestamo.objects.filter(ejemplar__isbn__isbn=isbn, miembro__id=id_miembro, estado_prestamo=True).first()
        
        if not prestamo:
            return Response({"error": "Préstamo no encontrado o ya devuelto"}, status=status.HTTP_404_NOT_FOUND)
        else:
            configuraciones = AppSettings.objects.all().first()
            pagoRetraso = 0
            pagoExtravio = 0

            # Comprobar si hay pagos por retraso
            if miembro.prestamo_set.filter(fecha_fin__lt=datetime.date.today(), estado_prestamo=True).count() > 0:
                dias = datetime.date.today() - prestamo.fecha_fin
                pagoRetraso = dias.days * configuraciones.cuota_mora

            # Comprobar si hay pago por extravío
            if id_estado == '4':
                pagoExtravio = configuraciones.cuota_extravio

            # Retornar la respuesta con los montos de pagoRetraso y pagoExtravio
            return Response({
                "mensaje": "Préstamo encontrado, puede proceder",
                "pagoRetraso": pagoRetraso,
                "pagoExtravio": pagoExtravio
            }, status=status.HTTP_200_OK)


class DevolucionView(APIView):
    def post(self, request):
        isbn = request.data.get("isbn")
        id_miembro = request.data.get("id_miembro")
        id_estado = request.data.get("id_estado")
        
        prestamo = Prestamo.objects.filter(ejemplar__isbn__isbn=isbn, miembro__id=id_miembro, estado_prestamo=True).first()
        
        #print(prestamo.id)

        if not prestamo:
            return Response({"error": "Préstamo no encontrado o ya devuelto"}, status=status.HTTP_404_NOT_FOUND)
        else:

            ejemplar = Ejemplar.objects.get(id=prestamo.ejemplar.id)
            
            if(id_estado == '4'):
                prestamo.recargo = True
                prestamo.save()

            prestamo.fecha_devolucion = datetime.date.today()
            prestamo.estado_prestamo = False
            prestamo.save()

            ejemplar.disponible = True
            ejemplar.estado_id = id_estado
            ejemplar.save()

        return Response({"mensaje": "Devolución realizada exitosamente"}, status=status.HTTP_200_OK)
    
class ListaPrestamosView(APIView):
    def get(self, request, format=None):
        prestamos = Prestamo.objects.select_related('miembro', 'ejemplar__isbn').all()
        data = []
        for prestamo in prestamos:
            # Verifica si el préstamo está vencido
            vencido = False
            if prestamo.fecha_fin < datetime.date.today() and prestamo.estado_prestamo:
                vencido = True

            data.append({
                'id_miembro': prestamo.miembro.id,
                'titulo_libro': prestamo.ejemplar.isbn.titulo,
                'fecha_prestamo': prestamo.fecha_inicio,
                'fecha_retorno': prestamo.fecha_fin,
                'vencido': vencido
            })
        return Response(data)