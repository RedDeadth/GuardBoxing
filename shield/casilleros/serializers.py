from rest_framework import serializers
from datetime import datetime

class CasilleroSerializer(serializers.Serializer):
    id = serializers.CharField(required=True) 
    location = serializers.CharField(required=False)  # Hacerlo opcional
    price = serializers.FloatField()
    open = serializers.BooleanField()
    blocked = serializers.BooleanField()
    occupied = serializers.BooleanField()
    
    description = serializers.CharField(required=False)  # Agrega 'description'
    sharedwith = serializers.ListField(child=serializers.CharField(), required=False)  # Campo adicional
    reservationEndTime = serializers.DateTimeField(required=False, allow_null=True)

    propietario = serializers.CharField(required=False)

    def get_reservationEndTime(self, obj):
        # Si existe reservationEndTime y es un timestamp en milisegundos
        if 'reservationEndTime' in obj:
            try:
                # Convertir de milisegundos a segundos y crear un datetime
                timestamp_seconds = int(obj['reservationEndTime']) / 1000
                return datetime.fromtimestamp(timestamp_seconds).isoformat()
            except (ValueError, TypeError):
                return None
        return None

    def to_representation(self, instance):
        # Primero obtenemos la representación estándar
        representation = super().to_representation(instance)
        
        # Eliminamos campos None o vacíos
        return {
            key: value for key, value in representation.items() 
            if value is not None and value != ''
        }
