from django.shortcuts import HttpResponse
from folium import Map, Marker, CircleMarker
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from .utils import sanitize, to_cordinates
from .serializer import MapCordinateSerializer

class MapViewSet(ViewSet):
    serializer_class = MapCordinateSerializer

    # /api/route-mapper/map
    def list(self, request):
         # get location from request url
        location = to_cordinates(
            sanitize(self.request.GET.get('location', None))
        )

        print(location)
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
        return HttpResponse(map._repr_html_())
