from django.urls import path
from . import views

app_name = 'casilleros'

urlpatterns = [
    path('lista/', views.casilleros_list, name='casilleros_list'),  # Vista para listar casilleros
    path('crear/', views.crear_casillero, name='crear_casillero'),  # Vista para crear un nuevo casillero
    path('detalle/<str:id>/', views.detalle_casillero, name='detalle_casillero'),  # Vista para los detalles del casillero
    path('bloquear/<str:id>/', views.bloquear_casillero, name='bloquear_casillero'),  # Vista para bloquear casillero
    path('abrir/<str:id>/', views.gestionar_apertura, name='gestionar_apertura'),  # Vista para abrir/cerrar casillero
   

    path('api/lista/', views.casilleros_list, name='api_casilleros_list'),  # API para listar casilleros
    path('api/crear/', views.crear_casillero, name='api_crear_casillero'),  # API para crear un nuevo casillero
    path('api/detalle/<str:id>/', views.detalle_casillero, name='api_detalle_casillero'),  # API para obtener detalles del casillero
    path('api/bloquear/<str:id>/', views.bloquear_casillero, name='api_bloquear_casillero'),  # API para bloquear casillero
    path('api/abrir/<str:id>/', views.gestionar_apertura, name='api_gestionar_apertura'),  # API para abrir/cerrar casillero
    
]