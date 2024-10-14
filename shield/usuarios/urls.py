# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar, name='registrar'),
    path('login/', views.login, name='login'),
    path('index/', views.index, name='index'),  # Ruta hacia la página de índice
    path('casilleros/', views.casilleros, name='casilleros'),  # Nueva ruta para casilleros.html
    path('detalle/<str:nombre>/<str:ubicacion>/<str:precio>/<str:descripcion>/', views.detalle, name='detalle'),
    path('logout/', views.logout, name='logout'),
]
