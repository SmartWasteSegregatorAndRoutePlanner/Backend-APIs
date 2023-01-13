from django.shortcuts import HttpResponse
from folium import Map, Marker, CircleMarker
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .utils import sanitize, to_cordinates, get_geojson_route_cordinates, plot_geojson_data_on_map


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
        print(json_data)
        locations = json_data.get('locations', [[]])
        print(locations)

        # extract locations and sort according to their weights

        resp = {
            'msg': 'locations data required in [ [lat1, long1], [lat2, long2,], ... ] format'
        }
        status_code = 400

        # create Map
        map = Map(location=locations[0], zoom_start=15)
            
        # get route co-ords
        geojson_data = get_geojson_route_cordinates(cordinates=locations)

        # plot data on map
        plot_geojson_data_on_map(geojson=geojson_data, map=map)

        # # add markers
        # Marker(
        #     location=start_latlng,
        #     tooltip='Start Location',
        #     popup=str(start_latlng)
        # ).add_to(shortest_route_map)

        # Marker(
        #     location=end_latlng,
        #     tooltip='End Location',
        #     popup=str(end_latlng)
        # ).add_to(shortest_route_map)

        # return map in html format
        return HttpResponse(map._repr_html_())



