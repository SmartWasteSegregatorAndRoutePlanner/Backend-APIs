from django.shortcuts import HttpResponse
from folium import Map, Marker, CircleMarker
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import sanitize, to_cordinates


# /api/route-mapper/map
class MapView(APIView):
    queryset = []

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

    def post(self, _):
        return Response({})
        if status_code != 400:
            # extract locations and sort according to their weights
            locations, status = to_sorted_locations_list(
                json_data.get('locations', [[]])
            )

            resp = {
                'msg': 'locations data required in [ [lat1, long1, node_weight1], [lat2, long2, node_weight2] ] format'}
            status_code = 400
            if status:
                print(locations)
                # TODO: write logic for finding shortest distance

                # define the start and end locations in latlng
                start_latlng = (37.78497, -122.43327)
                end_latlng = (37.78071, -122.41445)
                mode = 'drive' # 'drive', 'bike', 'walk'# find shortest path based on distance or time
                optimizer = 'length'# 'length','time'

                graph = ox.graph_from_point(
                    center_point=start_latlng, dist=4000, network_type=mode)

                # find the nearest node to the end location
                orig_nodes = ox.nearest_nodes(
                    graph, X=start_latlng[1], Y=start_latlng[0])
                dest_nodes = ox.nearest_nodes(
                    graph, X=end_latlng[1], Y=end_latlng[0] )  # find the shortest path

                shortest_route = nx.shortest_path(
                    graph,
                    orig_nodes,
                    dest_nodes,
                    weight=optimizer
                )

                # create map for shortest distance
                shortest_route_map = ox.plot_route_folium(graph, shortest_route, tiles='openstreetmap')

                # add markers
                folium.Marker(
                    location=start_latlng,
                    tooltip='Start Location',
                    popup=str(start_latlng)
                ).add_to(shortest_route_map)

                folium.Marker(
                    location=end_latlng,
                    tooltip='End Location',
                    popup=str(end_latlng)
                ).add_to(shortest_route_map)

                # add markers to starting and ending location
                return Response(text=shortest_route_map._repr_html_(), content_type='text/html', status=200)


                status_code = 200

