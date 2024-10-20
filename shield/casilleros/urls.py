from django.urls import path
from . import views

app_name = 'casilleros'

urlpatterns = [
    path('lista/', views.casilleros_list, name='casilleros_list'),
    path('api/lista/', views.lista_casilleros, name='api_lista_casilleros'), 
    path('crear/', views.crear_casillero, name='crear_casillero'),
    path('detalle/<str:id>/', views.detalle_casillero, name='detalle_casillero'),
    path('bloquear/<str:id>/', views.bloquear_casillero, name='bloquear_casillero'),
    path('abrir/<str:id>/', views.gestionar_apertura, name='gestionar_apertura'), 

    #url para comparitr el acceso por nickname
    path('compartir/<str:id>/', views.compartir_casillero, name='compartir_casillero'),

]