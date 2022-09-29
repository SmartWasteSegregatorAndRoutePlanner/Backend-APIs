from aiohttp.web import View, Response
from utils import sanitize, to_cordinates
import folium


class Maps(View):
    async def get(self):
        # get location from request url
        location = to_cordinates(
            sanitize(self.request.query.get('location', None))
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
