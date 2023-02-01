from django.shortcuts import HttpResponse
from folium import Map, Marker, CircleMarker
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .utils import sanitize, to_cordinates, get_route_data, plot_geojson_data_on_map, add_markers_to_map


import osmnx as ox
import networkx as nx

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

    def post(self, request: Request):
        json_data = request.data
        locations = json_data.get('locations', [[]])  # in [[lat, long]] format
        print(locations)

        # locations = ((80.21787585263182,6.025423265401452),(80.23929481745174,6.019639381180123))

        # create Map
        # map = Map(location=locations[0], zoom_start=30, control_scale=True)

        # # get route data
        # route_data, status_code = get_route_data(cordinates=locations)
        # print(route_data)

        # if status_code != 200:
        #     err = route_data
        #     return Response({'err':err})

        # # plot data on map
        # route_plot_map = plot_geojson_data_on_map(route_data=route_data, map=map)
        # print('GeoJSON data plotted')

        # # add markers
        # plot_map_with_marker = add_markers_to_map(co_ordinates=locations, map=route_plot_map)
        # print('-'*50)

        # # return map in html format
        # return HttpResponse(plot_map_with_marker._repr_html_())

        start_latlng = locations[0]
        end_latlng = locations[-1]
        mode = 'drive'  # 'drive', 'bike', 'walk'# find shortest path based on distance or time
        optimizer = 'length'  # 'length','time'

        graph = ox.graph_from_point(
            center_point=start_latlng, dist=4000, network_type=mode)

        # find the nearest node to the end location
        orig_nodes = ox.nearest_nodes(
            graph, X=start_latlng[1], Y=start_latlng[0])
        dest_nodes = ox.nearest_nodes(
            graph, X=end_latlng[1], Y=end_latlng[0])  # find the shortest path
        print(orig_nodes)
        print(dest_nodes)

        shortest_route = nx.shortest_path(
            graph,
            orig_nodes,
            dest_nodes,
            weight=optimizer
        )
        print(shortest_route)

        # TODO: visit each node once and plot route optimally
        # create map for shortest distance
        shortest_route_map = ox.plot_route_folium(
            graph, shortest_route, route_map=None, tiles='openstreetmap')

        # add markers
        Marker(
            location=start_latlng,
            tooltip='Start Location',
            popup=str(start_latlng)
        ).add_to(shortest_route_map)

        Marker(
            location=end_latlng,
            tooltip='End Location',
            popup=str(end_latlng)
        ).add_to(shortest_route_map)

        return HttpResponse(shortest_route_map._repr_html_())
