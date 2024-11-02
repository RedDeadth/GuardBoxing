from rest_framework import serializers
from datetime import datetime

class CasilleroSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    location = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    price = serializers.FloatField(required=False, allow_null=True)
    open = serializers.BooleanField(default=False)
    blocked = serializers.BooleanField(default=False)
    occupied = serializers.BooleanField(default=False)
    
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    sharedwith = serializers.ListField(
        child=serializers.CharField(), 
        required=False, 
        allow_null=True,
        default=list
    )
    reservationEndTime = serializers.DateTimeField(required=False, allow_null=True)
    propietario = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def get_reservationEndTime(self, obj):
        # Si no existe reservationEndTime o es nulo, retornamos None
        if not obj.get('reservationEndTime'):
            return None
            
        try:
            # Convertir de milisegundos a segundos y crear datetime
            timestamp_seconds = int(obj['reservationEndTime']) / 1000
            return datetime.fromtimestamp(timestamp_seconds).isoformat()
        except (ValueError, TypeError):
            return None

    def to_representation(self, instance):
        # Manejar tanto diccionarios como instancias de modelo
        data = instance if isinstance(instance, dict) else instance.__dict__
        
        # Crear representación con valores por defecto para campos faltantes
        representation = {
            'id': data.get('id'),
            'location': data.get('location', ''),
            'price': data.get('price'),
            'open': data.get('open', False),
            'blocked': data.get('blocked', False),
            'occupied': data.get('occupied', False),
            'description': data.get('description', ''),
            'sharedwith': data.get('sharedwith', []),
            'reservationEndTime': self.get_reservationEndTime(data),
            'propietario': data.get('propietario', '')
        }
        
        # Eliminar valores None o vacíos
        return {
            key: value for key, value in representation.items() 
            if value is not None and value != ''
        }