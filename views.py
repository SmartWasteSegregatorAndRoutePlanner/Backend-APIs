from aiohttp.web import View, Response
from utils import sanitize, to_cordinates, get_json_data, create_json_response, to_sorted_locations_list
from rate_limiter import limiter

import folium
import osmnx as ox
import networkx as nx

# ox.config(use_cache=True, log_console=True)
ox.settings.log_console = True
ox.settings.use_cache = True


class Maps(View):
    @limiter.limit(ratelimit="1/second")
    async def get(self):
        '''
        ---
        description: This endpoint allows user to load maps marking specified location
        tags:
        - Map
        produces:
        - application/json
        - text/html
        parameters:
        -   in: query
            name: location
            description: latitude,longitude value seperated by comma to indicate location
            schema:
                type: float
            required: false
        responses:
            "200":
                description: successful operation. Returns html page with map
            "405":
                description: Method Not allowed
            "429":
                description: Rate limit exceeded
        '''
        # get location from request url
        location = to_cordinates(
            sanitize(self.query.get('location', None))
        )

        # create map using location
        map = folium.Map(location=location, zoom_start=15)

        # add markers
        folium.Marker(
            location=location,
            popup='location',
            tooltip=str(location)
        ).add_to(map)
        folium.CircleMarker(
            location=location,
            radius=10
        ).add_to(map)

        # return map in html format
        return Response(text=map._repr_html_(), content_type='text/html', status=200)

    @limiter.limit(ratelimit="1/second")
    async def post(request):
        '''
        ---
        description: This endpoint allows user to load maps and calculate optimal path between various locations
        tags:
        - Map
        produces:
        - application/json
        - text/html
        parameters:
        -   in: body
            name: locations
            description: array containing latitude, longitude and node weightage values seperated by comma to indicate location
            schema:
                type: object
                properties:
                    locations:
                        type: array
                        items:
                            type: array
                            items:
                                type: number
                                format: double
                items:
                    type: array
            required: true
        responses:
            "200":
                description: On successful operation returns html page with optimal path on map
            "400":
                description: JSON format is invalid or request cannot be processed
            "405":
                description: Method Not allowed
        '''
        json_data, status_code = await get_json_data(request)
        if status_code != 400:
            # extract locations and sort according to their weights
            locations, status = to_sorted_locations_list(
                json_data.get('locations', [[]])
            )

            resp = {
                'msg': 'locations data required in [ [lat1, long1, node_weight1], [lat2, long2, node_weight2] ] format'}
            status_code = 400
            if status:
                # resp = sorted(locations, key=lambda location: location[2])
                # status_code = 200

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

              

        return create_json_response(resp, status_code)
