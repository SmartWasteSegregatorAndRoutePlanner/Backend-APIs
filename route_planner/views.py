from django.shortcuts import HttpResponse
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from folium import Map, Marker, CircleMarker
from itertools import combinations
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.request import Request
from rest_framework.response import Response


from .utils import sanitize, to_cordinates, add_locations_to_map, get_shortest_distance
from .models import GarbageBinLocation
from .serializer import GarbageBinLocationSerializer


import osmnx as ox
import networkx as nx
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] [%(levelname)s] - %(message)s')


# Global variable to store routes between location
routes = dict()

# HTTP Method: class function
# GET: list
# POST: create
# PUT: update
# PATCH: partial_update
# DELETE: destroy

# Endpoint
# /api/route-mapper/map


class MapViewSet(ReadOnlyModelViewSet):
    queryset = GarbageBinLocation.objects.all()
    serializer_class = GarbageBinLocationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # cache requested url for each user for 2 hours
    @method_decorator(cache_page(60*60*2))
    def create(self, request):
        '''
        HTTP POST request 
        '''
        # get location from request url
        location = to_cordinates(
            sanitize(request.GET.get('location', None))
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

    # cache requested url for each user for 1 hour
    @method_decorator(cache_page(60*60*1))
    def list(self, _: Request):
        '''
        HTTP GET request returns optimal route direction map visiting 
        all GarbageBinLocations
        '''
        locations = self.get_queryset()

        start_loc: GarbageBinLocation = locations[0]
        end_loc: GarbageBinLocation = locations[1]

        start_latlng = (start_loc.latitude, start_loc.longitude)
        end_latlng = (end_loc.latitude, end_loc.longitude)

        mode = 'drive'  # 'drive', 'bike', 'walk'# find shortest path based on distance or time
        optimizer = 'length'  # 'length','time'

        # create graph from point
        graph = ox.graph_from_point(
            center_point=start_latlng, dist=4000, network_type=mode)

        # find the nearest node to the end location
        orig_nodes = ox.nearest_nodes(
            graph, X=start_latlng[1], Y=start_latlng[0])
        dest_nodes = ox.nearest_nodes(
            graph, X=end_latlng[1], Y=end_latlng[0])  # find the shortest path

        shortest_route = nx.shortest_path(
            graph,
            orig_nodes,
            dest_nodes,
            weight=optimizer
        )

        # TODO: visit each node once and plot route optimally
        # create map for shortest distance
        shortest_route_map = ox.plot_route_folium(
            graph, shortest_route, route_map=None, tiles='openstreetmap')

        # add markers
        shortest_route_map = add_locations_to_map(
            locations=locations, map=shortest_route_map)

        return HttpResponse(shortest_route_map._repr_html_())


# /api/route-mapper/update-routes
@api_view(['GET'])
def update_routes_data(request):
    '''
    Apply Djikstra's algorithm and store result in global variable which will be 
    used when user sends GET request on /api/route-mapper/map endpoint
    '''
    # call this endpoint after updating GarbageBinLocations data from Admin panel to
    # update routes global variable
    global routes

    status_code = 201
    msg = 'Routes Updated'
    try:
        # create routes from every location to another location in local memory
        garbage_bin_locations: list[GarbageBinLocation] = set(
            GarbageBinLocation.objects.all())

        # map routes between garbage_bin_locations
        for src_dst_pair in combinations(garbage_bin_locations, 2):
            # extract src and dst nodes
            src_gb_loc = src_dst_pair[0]
            trgt_gb_loc = src_dst_pair[1]

            # calculate route and store it global variable
            shortest_distance = get_shortest_distance(
                start_loc=src_gb_loc, end_loc=trgt_gb_loc)
            route = {trgt_gb_loc.name: shortest_distance}
            routes[src_gb_loc.name] = route
            logging.debug(
                f'Route Calculated Between {src_gb_loc.name} - {trgt_gb_loc.name}')

    except Exception as e:
        msg = 'Error, Check logs for more info'
        status_code = 500

    return Response({'msg': msg}, status=status_code, content_type='application/json')
