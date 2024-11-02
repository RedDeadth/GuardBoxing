# urls.py

from django.urls import path
from . import views
from .views import get_current_user

urlpatterns = [
    path('registrar/', views.registrar, name='registrar'),
    path('login/', views.login, name='login'),
    path('get_current_user/', get_current_user, name='get_current_user'),  
    path('index/', views.index, name='index'),  # Ruta hacia la página de índice
    path('casilleros/', views.casilleros, name='casilleros'),  # Nueva ruta para casilleros.html
    path('detalle/<str:nombre>/<str:ubicacion>/<str:precio>/<str:descripcion>/', views.detalle, name='detalle'),
    path('logout/', views.logout, name='logout'),
]
