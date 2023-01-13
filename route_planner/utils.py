from backend_api.settings import ORS_API_KEY
from folium import GeoJson, Map
from openrouteservice import Client
from openrouteservice.exceptions import ApiError
from openrouteservice.convert import decode_polyline
from html import escape


def to_cordinates(location: str, default: tuple[float] = (28.653458, 77.123767)):
    assert isinstance(location, str)

    co_ords = default
    try:
        lat, long = [float(pos) for pos in location.split(',')]
        co_ords = (lat, long) or default
    except ValueError:
        pass

    return co_ords


def plot_geojson_data_on_map(geojson, map: Map) -> Map:
    # add default value to avoid errs
    routes = geojson.get('routes', [{'geometry': '_zwc@mqrhNLALANhA@HNpAcEv@m@J}A\\wAXqA\\aAPkGZe@BKDA@C?A?KEaAHI?c@@QDMDUHABC?C@CAC?GGAC?C@EGgAOc@ISO[c@SCACCCC_@UOC}@MaAOSAUBa@HCBCBK?ICCCACw@cAGGMKY[w@u@QS}@eAsAiBo@{@]c@MQ_@g@w@kAe@u@gA_CyAmD{@gCk@qBe@kBg@{DGs@E{EE_BESIYSUIGEC]WGSCM@UHo@`@yB@IXiAb@yAl@gBHQ`AkBxAmCt@uAPc@Zo@Zs@@EBGNm@N{@Fq@BS@QHk@Ji@^cA^aAlAwC^aAn@eCF]P}An@eGHa@FSJYVi@n@cAx@}@dB{A|@aAdA_AlA}@l@c@PWROl@e@\\WTQt@s@r@q@JIl@s@Zc@nA_Bb@e@TSDAXO^Y~@m@`Ag@NGZQTMpAy@FHFF?Xw@nBCN@JJDz@RXDNAJEFIBORW\\OXJx@vAL`AFNTTbAf@l@\\~A`@jC^fAHnAV`BZl@FbAJrAD`CJ~BVl@?'}])

    # plot routes on map
    for route in routes:
        geometry = route.get('geometry')

        # decode polyline and add to map
        decoded = decode_polyline(geometry)
        GeoJson(decoded).add_to(map)

    return map


def get_geojson_route_cordinates(cordinates: list[list[float]]):
    assert isinstance(cordinates, list)

    # sanitize co-ordinates to prevent injection attacks
    for co_ordinate in cordinates:
        try:
            lat = float(co_ordinate[0])
            long = float(co_ordinate[1])
            co_ordinate = [lat, long]
        except ValueError:
            del co_ordinate

    # make request and get directions geojson data
    status = 200
    client = Client(key=ORS_API_KEY)
    try:
        geojson_data = client.directions(cordinates)
    except ApiError as e:
        geojson_data = dict(e.message).get('error', {
            'error':'try co-ordinates with shorter distance'
        })
        status = 404

    return geojson_data, status


def add_markers(co_ordinates: list[list[float]], map: Map):
    pass


def sanitize(data: str) -> str:
    return escape(str(data))
