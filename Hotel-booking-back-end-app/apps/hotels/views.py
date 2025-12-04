# apps/locations/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Location
from .serializers import LocationTreeSerializer

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationTreeSerializer

    # GET /locations/tree
    def list(self, request, *args, **kwargs):
        roots = Location.objects.filter(parent=None)
        serializer = self.get_serializer(roots, many=True)
        return Response(serializer.data)

    # GET /locations/{id}/children
    def children(self, request, pk=None):
        location = self.get_object()
        children = location.children.all()
        serializer = self.get_serializer(children, many=True)
        return Response(serializer.data)
