from rest_framework import serializers

class CasilleroSerializer(serializers.Serializer):
    id = serializers.CharField(source='key', read_only=True)
    location = serializers.CharField(required=False)  # Hacerlo opcional
    price = serializers.FloatField()
    open = serializers.BooleanField()
    blocked = serializers.BooleanField()
    occupied = serializers.BooleanField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = instance.get('id', None)  # Usar get para evitar KeyError
        return representation
