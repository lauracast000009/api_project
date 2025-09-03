from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Persona, Tarea
from .serializers import PersonaSerializer
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date

# Acciones a realizar para cada endponit pedido en la actividad
# Listar personas
class PersonaList(generics.ListAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

    def get(self, request, *args, **kwargs):
        personas = Persona.objects.all()
        if not personas:
            raise NotFound('No se encontraron personas')
        serializer = PersonaSerializer(personas, many=True)
        return Response(
            {
                'success': True,
                'detail': 'Listado de personas',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

# Eliminar persona
class EliminarPersona(generics.DestroyAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

    def delete(self, request, pk, *args, **kwargs):
        persona = get_object_or_404(Persona, pk=pk)
        persona.delete()
        return Response(
            {
                'success': True,
                'detail': 'Persona eliminada correctamente'
            },
            status=status.HTTP_204_NO_CONTENT
        )


#  Crear persona
class CrearPersona(generics.CreateAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

    def post(self, request, *args, **kwargs):
        serializer = PersonaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'success': True,
                'detail': 'Persona creada correctamente',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED
        )


#  Actualizar persona
class ActualizarPersona(generics.UpdateAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

    def put(self, request, pk):
        persona = get_object_or_404(Persona, pk=pk)
        email = request.data.get('email', None)

        #verificar si email cambio
        if email and email != persona.email:
            #verificar si existe ese correo
            if Persona.objects.filter(email=email).exclude(pk=pk).exists():
                return Response({'email':['Ya existe ese correo']},status=status.HTTP_400_BAD_REQUEST)
            
        serializer = PersonaSerializer(persona, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'success': True,
                'detail': 'Persona actualizada correctamente',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

# buscar persona por documento

class PersonaByDocumento(generics.ListAPIView):
    serializer_class = PersonaSerializer

    def get(self, request, documento):
        persona = Persona.objects.filter(documento=documento).first()
        if not persona:
            raise NotFound('No se encontra una persona en ese documento')
        serializer = PersonaSerializer(persona)
        return Response({'success':True,'detail':'Persona encontrada','data':serializer.data},status=status.HTTP_200_OK)


from .models import Tarea
from .serializers import TareaSerializer
from django.utils.dateparse import parse_date


# Eliminar tarea
class EliminarTarea(generics.DestroyAPIView):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer

    def delete(self, request, pk, *args, **kwargs):
        tarea = get_object_or_404(Tarea, pk=pk)
        tarea.delete()
        return Response(
            {
                'success': True,
                'detail': 'Tarea eliminada correctamente'
            },
            status=status.HTTP_204_NO_CONTENT
        )


# Listar y crear tareas
class TareaList(generics.ListCreateAPIView):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer


# Buscar tareas por fecha exacta
class TareaByFecha(generics.ListAPIView):
    serializer_class = TareaSerializer

    def get(self, request, fecha):
        tareas = Tarea.objects.filter(fecha_limite=parse_date(fecha))
        if not tareas:
            raise NotFound('No se encontraron tareas en esa fecha')
        serializer = TareaSerializer(tareas, many=True)
        return Response(
            {'success': True, 'detail': 'Tareas encontradas', 'data': serializer.data},
            status=status.HTTP_200_OK
        )


# Buscar tareas por rango de fechas
class TareaByRangoFechas(generics.ListAPIView):
    serializer_class = TareaSerializer

    def get(self, request, fecha_inicio, fecha_fin):
        tareas = Tarea.objects.filter(
            fecha_limite__range=[parse_date(fecha_inicio), parse_date(fecha_fin)]
        )
        if not tareas:
            raise NotFound('No se encontraron tareas en ese rango de fechas')
        serializer = TareaSerializer(tareas, many=True)
        return Response(
            {'success': True, 'detail': 'Tareas encontradas', 'data': serializer.data},
            status=status.HTTP_200_OK
        )


# Buscar tareas por persona
class TareaByPersona(generics.ListAPIView):
    serializer_class = TareaSerializer

    def get(self, request, id_persona):
        tareas = Tarea.objects.filter(persona_id=id_persona)
        if not tareas:
            raise NotFound('No se encontraron tareas para esa persona')
        serializer = TareaSerializer(tareas, many=True)
        return Response(
            {'success': True, 'detail': 'Tareas encontradas', 'data': serializer.data},
            status=status.HTTP_200_OK
        )
# Actualizar tarea
class ActualizarTarea(generics.UpdateAPIView):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer

    def put(self, request, pk, *args, **kwargs):
        tarea = get_object_or_404(Tarea, pk=pk)
        serializer = TareaSerializer(tarea, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'success': True,
                'detail': 'Tarea actualizada correctamente',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
