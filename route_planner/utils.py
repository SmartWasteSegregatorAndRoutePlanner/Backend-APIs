from folium import Map, Marker
from html import escape
from .models import GarbageBinLocation


import osmnx as ox
import networkx as nx


def to_cordinates(location: str, default: tuple[float] = (28.653458, 77.123767)):
    assert isinstance(location, str)

    co_ords = default
    try:
        lat, long = [float(pos) for pos in location.split(',')]
        co_ords = (lat, long) or default
    except ValueError:
        pass

    return co_ords


def add_locations_to_map(locations: list[GarbageBinLocation], map: Map):
    for location in locations:
        coordinate = (location.latitude, location.longitude)
        Marker(
            location=coordinate,
            tooltip=location.name,
            popup=str(coordinate)
        ).add_to(map)

    return map


def sanitize(data: str) -> str:
    return escape(str(data))

def get_shortest_distance(start_loc:GarbageBinLocation, end_loc:GarbageBinLocation):
    '''
    Returns shortest distance between two Garbage Bin locations
    '''
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
    
    try:
        shortest_route = nx.shortest_path(
            graph,
            orig_nodes,
            dest_nodes,
            weight=optimizer
        )
    except nx.exception.NetworkXNoPath:
        shortest_route = None
        
    return shortest_route