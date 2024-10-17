from django.urls import path
from . import views

app_name = 'casilleros'

urlpatterns = [
    path('lista/', views.casilleros_list, name='casilleros_list'),
    path('api/lista/', views.lista_casilleros, name='api_lista_casilleros'), 
    path('crear/', views.crear_casillero, name='crear_casillero'),
    path('detalle/<str:id>/', views.detalle_casillero, name='detalle_casillero'),
    path('bloquear/<str:id>/', views.bloquear_casillero, name='bloquear_casillero'),
    path('cambiar-apertura/<str:id>/', views.cambiar_apertura, name='cambiar_apertura'),
      # Ruta para la API
]