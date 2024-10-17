from rest_framework import serializers
from .models import Casillero  # Asegúrate de que Casillero sea el modelo adecuado

class CasilleroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Casillero
        fields = ['id', 'nombre', 'ubicacion', 'precio', 'descripcion', 'estado', 'apertura']  # Añade los campos que desees
