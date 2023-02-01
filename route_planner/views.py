from django.shortcuts import HttpResponse
from folium import Map, Marker, CircleMarker
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .utils import sanitize, to_cordinates, get_route_data, plot_geojson_data_on_map, add_markers_to_map


# /api/route-mapper/map
class MapView(APIView):
    # parse JSON data automatically
    parser_classes = [JSONParser]

    def get(self, _):
        # get location from request url
        location = to_cordinates(
            sanitize(self.request.GET.get('location', None))
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
        return HttpResponse(map._repr_html_())

    def post(self, request:Request):
        json_data = request.data
        locations = json_data.get('locations', [[]]) # in [[lat, long]] format
        print(locations)

        # locations = ((80.21787585263182,6.025423265401452),(80.23929481745174,6.019639381180123))

        # create Map
        map = Map(location=locations[0], zoom_start=30, control_scale=True)
            
        # get route data
        route_data, status_code = get_route_data(cordinates=locations)
        print(route_data)

        if status_code != 200:
            err = route_data
            return Response({'err':err})
            
        # plot data on map
        route_plot_map = plot_geojson_data_on_map(route_data=route_data, map=map)
        print('GeoJSON data plotted')

        # add markers
        plot_map_with_marker = add_markers_to_map(co_ordinates=locations, map=route_plot_map)
        print('-'*50)

        # return map in html format
        return HttpResponse(plot_map_with_marker._repr_html_())



