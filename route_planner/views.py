from django.shortcuts import HttpResponse
# from django.views.decorators.cache import cache_page
# from django.utils.decorators import method_decorator
from folium import Map, Marker, CircleMarker
from itertools import combinations
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from pprint import pprint

from .utils import sanitize, to_cordinates, add_locations_to_map, get_shortest_distance, save_routes, read_routes
from .models import GarbageBinLocation
from .serializer import GarbageBinLocationSerializer


import osmnx as ox
import networkx as nx
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)s] - %(message)s')


# Global variable to store routes between location
routes = dict()
routes = read_routes()

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
    # @method_decorator(cache_page(60*60*2))
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
    # @method_decorator(cache_page(60*60*1))
    def list(self, _: Request):
        '''
        HTTP GET request returns optimal route direction map visiting
        all GarbageBinLocations
        '''
        if not routes:
            return Response({'msg': 'Update Routes before sending request to this endpoint'}, status=500, content_type='application/json')

        locations = self.get_queryset()

        # remove empty garbage bin locations
        locations = list(filter(lambda loc: loc.garbage_weight > 0, locations))
        logger.debug(f'Filtered Locations: {locations}')

        # TODO: consider locations and apply djikstra's algorithm between locations
        center_loc = locations[0]
        center_loc = (center_loc.latitude, center_loc.longitude)
        # BUG: If you're getting some sort of key error then increase distance value
        graph: nx.classes.multidigraph.MultiDiGraph = ox.graph_from_point(
            center_point=center_loc, dist=10000, network_type='drive')
        logging.info(f'Center Location: {locations[0]}')

        # create base map
        shortest_route_map = Map(location=center_loc)

        # consider minimum distance as optimal path using djikstra's algorithm
        for src_location in routes.keys():
            for dst_location in routes[src_location].keys():
                
                # TODO: Use Kruksal's algorithm to find minimum spanning tree and then plot routes 
                route = None

                # plot route on map if present
                if route:
                    shortest_route_map = ox.plot_route_folium(
                        G=graph, route=route, route_map=shortest_route_map, tiles='openstreetmap')
                    logger.info(
                        f'Route plotted between {src_location} - {dst_location}')

        # add markers
        shortest_route_map = add_locations_to_map(
            locations=locations, map=shortest_route_map)

        return HttpResponse(shortest_route_map._repr_html_())


# /api/route-mapper/update-routes
@api_view(['GET'])
# @cache_page(60*60*1)
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
            distance = ox.distance.great_circle_vec(
                src_gb_loc.latitude, src_gb_loc.longitude, trgt_gb_loc.latitude, trgt_gb_loc.longitude)

            # get and update previous data
            route = routes.get(src_gb_loc.name, {})
            route[trgt_gb_loc.name] = {
                'path': shortest_distance,
                'distance': distance
            }
            routes[src_gb_loc.name] = route
            logging.info(
                f'Route Calculated Between {src_gb_loc.name} - {trgt_gb_loc.name}, distance: {distance}')
        save_routes(routes)

    except Exception:
        msg = 'Error, Check logs for more info'
        status_code = 500

    return Response({'msg': msg}, status=status_code, content_type='application/json')
