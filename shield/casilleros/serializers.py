from rest_framework import serializers

class CasilleroSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    nombre = serializers.CharField(required=False, allow_blank=True)
    ubicacion = serializers.CharField(required=False, allow_blank=True)
    precio = serializers.CharField(required=False, allow_blank=True)
    descripcion = serializers.CharField(required=False, allow_blank=True)
    estado = serializers.CharField(required=False, allow_blank=True)
    apertura = serializers.CharField(required=False, allow_blank=True)

    def to_representation(self, instance):
        # Comenzar con una representación que incluye todos los campos
        ret = {
            'id': self.context.get('id', ''),
            'nombre': '',
            'ubicacion': '',
            'precio': '',
            'descripcion': '',
            'estado': '',
            'apertura': ''
        }
        # Actualizar con los valores reales del instance, si existen
        ret.update({k: v for k, v in instance.items() if v is not None})
        return ret