from django.shortcuts import render
from folium import Map, Marker, CircleMarker
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from .utils import sanitize, to_cordinates
from .serializer import MapCordinateSerializer

class MapViewSet(ViewSet):
    serializer_class = MapCordinateSerializer

    # TODO: endpoint isn't mapped correctly
    def list(self, request):
         # get location from request url
        location = to_cordinates(
            sanitize(self.request.query.get('location', None))
        )

        # create map using location
        map = Map(location=location, zoom_start=15)

        # add markers
        Marker(
            location=location,
            popup='location',
            tooltip=str(location)
        ).add_to(map)
        CircleMarker(
            location=location,
            radius=10
        ).add_to(map)

        # return map in html format
        return render(request, map._repr_html_())
