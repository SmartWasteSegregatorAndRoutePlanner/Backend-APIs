from aiohttp.web import View, Response
from utils import sanitize, to_cordinates, get_json_data, create_json_response, to_sorted_locations_list
from rate_limiter import limiter

import folium


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
    async def post(self):
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
        json_data, status_code = await get_json_data(self.request)
        if status_code != 400:
            # extract locations and sort according to their weights
            locations, status = to_sorted_locations_list(
                json_data.get('locations', [[]])
            )

            resp = {
                'msg': 'locations data required in [ [lat1, long1, node_weight1], [lat2, long2, node_weight2] ] format'}
            status_code = 400
            if status:
                resp = sorted(locations, key=lambda location: location[2])
                status_code = 200

                # create map using location
                # map = folium.Map(location=location, zoom_start=15)

                # add markers
                # folium.Marker(
                #     location=location,
                #     popup='location',
                #     tooltip=str(location)
                # ).add_to(map)
                # folium.CircleMarker(
                #     location=location,
                #     radius=10
                # ).add_to(map)

                # return map in html format
                # return Response(text=map._repr_html_(), content_type='text/html', status=200)
        return create_json_response(resp, status_code)
