# urls.py

from django.urls import path
from . import views
from .views import verificar_token

urlpatterns = [
    path('registrar/', views.registrar, name='registrar'),
    path('login/', views.login, name='login'),
    path('index/', views.index, name='index'),  # Ruta hacia la página de índice
    path('casilleros/', views.casilleros, name='casilleros'),  # Nueva ruta para casilleros.html
    
    path('logout/', views.logout, name='logout'),

    path('verificar_token/', verificar_token, name='verificar_token'),
]
