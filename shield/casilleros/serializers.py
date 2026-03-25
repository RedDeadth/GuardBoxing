from rest_framework import serializers

class CasilleroSerializer(serializers.Serializer):
    id = serializers.CharField(required=True) 
    location = serializers.CharField(required=False)
    price = serializers.FloatField()
    open = serializers.BooleanField()
    blocked = serializers.BooleanField()
    userId = serializers.CharField(required=False, allow_null=True)
    userEmail = serializers.CharField(required=False, allow_null=True)
    userName = serializers.CharField(required=False, allow_null=True)
    
    description = serializers.CharField(required=False)
    sharedwith = serializers.ListField(child=serializers.CharField(), required=False)
    reservationendtime = serializers.DateTimeField(required=False, allow_null=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = instance.get('id', None)
        return representation
