from rest_framework import serializers

class CasilleroSerializer(serializers.Serializer):
    id = serializers.CharField(required=True) 
    location = serializers.CharField(required=False)  # Hacerlo opcional
    price = serializers.FloatField()
    open = serializers.BooleanField()
    blocked = serializers.BooleanField()
    occupied = serializers.BooleanField()
    
    description = serializers.CharField(required=False)  # Agrega 'description'
    sharedwith = serializers.ListField(child=serializers.CharField(), required=False)  # Campo adicional
    reservationendtime = serializers.DateTimeField(required=False, allow_null=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = instance.get('id', None)  # Usar get para evitar KeyError
        return representation
