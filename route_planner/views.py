from django.shortcuts import HttpResponse
from folium import Map, Marker, CircleMarker
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .utils import sanitize, to_cordinates, get_geojson_route_cordinates, plot_geojson_data_on_map, add_markers_to_map


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
        # geojson_data, status_code = get_geojson_route_cordinates(cordinates=locations)

        # if status_code != 200:
        #     err = geojson_data
        #     return Response({'err':err})
            
        # plot data on map
        # plot_geojson_data_on_map(geojson=geojson_data, map=map)


        # add markers
        add_markers_to_map(co_ordinates=locations, map=map)

        # return map in html format
        return HttpResponse(map._repr_html_())



