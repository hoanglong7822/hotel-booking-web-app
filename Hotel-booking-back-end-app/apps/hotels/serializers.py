from rest_framework import serializers
from .models import Location

class LocationTreeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = ['id', 'name', 'type', 'children']

    def get_children(self, obj):
        if obj.children.exists():
            return LocationTreeSerializer(obj.children.all(), many=True).data
        return []
