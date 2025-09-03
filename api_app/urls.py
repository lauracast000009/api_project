from django.urls import path, include
from django.contrib import admin

from .views import (
    PersonaList, PersonaByDocumento, ActualizarPersona, CrearPersona, EliminarPersona,
    TareaList, TareaByFecha, TareaByRangoFechas, TareaByPersona,EliminarTarea,ActualizarTarea,
)

urlpatterns = [
   
    # Personas
    path('personas/', PersonaList.as_view(), name='persona-list'),
    path('personas/crear/', CrearPersona.as_view(), name='persona-crear'),
    path('personas/actualizar/<int:pk>/', ActualizarPersona.as_view(), name='persona-actualizar'),
    path('personas/documento/<str:documento>/', PersonaByDocumento.as_view(), name='persona-por-documento'),
    path('personas/eliminar/<int:pk>/', EliminarPersona.as_view(), name='persona-eliminar'),



    #Tareas
    path('tareas/', TareaList.as_view(), name='tarea-list'),
    path('tareas/fecha/<str:fecha>/', TareaByFecha.as_view(), name='tarea-por-fecha'),
    path('tareas/rango/<str:fecha_inicio>/<str:fecha_fin>/', TareaByRangoFechas.as_view(), name='tarea-por-rango'),
    path('tareas/actualizar/<int:pk>/', ActualizarTarea.as_view(), name='tarea-actualizar'),
    path('tareas/persona/<int:id_persona>/', TareaByPersona.as_view(), name='tareas-por-persona'),
    path('tareas/eliminar/<int:pk>/', EliminarTarea.as_view(), name='tarea-eliminar'),
]
