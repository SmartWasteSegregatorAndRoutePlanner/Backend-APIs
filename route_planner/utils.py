from backend_api.settings import ORS_API_KEY
from folium import GeoJson, Map, Marker
from openrouteservice import Client
from openrouteservice.exceptions import ApiError
from openrouteservice.convert import decode_polyline
from html import escape
from .models import GarbageBinLocation


import osmnx as ox
import networkx as nx

# ors client
ors_client = Client(key=ORS_API_KEY)


def to_cordinates(location: str, default: tuple[float] = (28.653458, 77.123767)):
    assert isinstance(location, str)

    co_ords = default
    try:
        lat, long = [float(pos) for pos in location.split(',')]
        co_ords = (lat, long) or default
    except ValueError:
        pass

    return co_ords


def plot_geojson_data_on_map(route_data:dict, map: Map) -> Map:
    # add default value to avoid errs
    # routes = geojson.get('routes', [{'geometry': '_zwc@mqrhNLALANhA@HNpAcEv@m@J}A\\wAXqA\\aAPkGZe@BKDA@C?A?KEaAHI?c@@QDMDUHABC?C@CAC?GGAC?C@EGgAOc@ISO[c@SCACCCC_@UOC}@MaAOSAUBa@HCBCBK?ICCCACw@cAGGMKY[w@u@QS}@eAsAiBo@{@]c@MQ_@g@w@kAe@u@gA_CyAmD{@gCk@qBe@kBg@{DGs@E{EE_BESIYSUIGEC]WGSCM@UHo@`@yB@IXiAb@yAl@gBHQ`AkBxAmCt@uAPc@Zo@Zs@@EBGNm@N{@Fq@BS@QHk@Ji@^cA^aAlAwC^aAn@eCF]P}An@eGHa@FSJYVi@n@cAx@}@dB{A|@aAdA_AlA}@l@c@PWROl@e@\\WTQt@s@r@q@JIl@s@Zc@nA_Bb@e@TSDAXO^Y~@m@`Ag@NGZQTMpAy@FHFF?Xw@nBCN@JJDz@RXDNAJEFIBORW\\OXJx@vAL`AFNTTbAf@l@\\~A`@jC^fAHnAV`BZl@FbAJrAD`CJ~BVl@?'}])

    # plot routes on map
    ##  decode polyline and add to map
    geometry = route_data.get('geometry', 'mtkeHuv|q@kA{@WWIUAU?SDMHMl@[HIDMDYDq@DMLIz@EHCLSBW?MGY_AyBKOECSFe@FQA]EkAWWMk@e@W_@mAmAe@e@WSWW@LJ~C@r@CTYzAeAzEWrBSfA]lAq@zAUp@KXsANQEYNY@WNMAKb@[jAQpAOj@Ab@u@n@]V]LGs@EUa@c@kAm@iBcC_E{D{@_@wAaAa@u@m@sBw@s@yAUEYi@vAh@wADXxATv@r@l@rB`@t@vA`Az@^~DzDhBbCjAl@`@b@DTFr@}@Mk@GuB@c@EsAc@a@Gq@EmBPi@Rq@b@UTI\\ItAE`@TrAAj@BZp@dCPd@R`@x@dEF`AHFHNBh@^~AXvAH`@h@fDGB[XSZyCrFW\\wAx@WTWXQZ_@fAMPUPWJuAVw@XiAh@URYOMGM[kAkEYiB]}@s@sASWUOaA`Bs@j@MPi@pBU^Y\\[\\YXQLCBWLW@WEYM[MGXoArEiAlC_AhCw@|B[p@a@l@g@f@g@XWNmAn@{@V}A\\wATU@UEoAe@aAUiBIWG]MK}@_@mC[oAU{A]w@S]U_@USwAy@OOQSg@u@u@c@m@Ok@A{BJmBXqBkBsA}@{Ao@eB@]GKIMKO_@a@_CQi@AEI]c@iBQi@Qc@kAyBWS_@SaAE{@yAu@mDUsAqA}@EM@QTiA|@iAn@gAd@eAg@_@I]??k@i@yBkEa@}@W}@WkCUqC?_@Hg@ZqABg@Gm@YoAEgAMq@@jAB|CC`@{@rACHBIz@sABa@C}CAkALp@DfAXnAFl@Cf@[pAIf@?^TpCVjCV|@`@|@xBjEj@h@??H\\f@^e@dAo@fA}@hAUhAAPDLpA|@TrAt@lDz@xA`AD^RVRjAxBPb@Ph@b@hBH\\@DPh@`@~BN^LJJH\\FdBAzAn@rA|@pBjBlBYzBKj@@l@Nt@b@f@t@PRNNvAx@TRT^R\\\\v@TzAZnA^lCJ|@\\LVFhBH`ATnAd@TDTAvAU|A]z@WlAo@VOf@Yf@g@`@m@Zq@v@}B~@iChAmCnAsEFYZLXLVDVAVMBCPMXYZ]X]T_@h@qBLQr@k@`AaBTNRVr@rA\\|@XhBjAjELZLFXNTShAi@v@YtAWVKTQLQ^gAP[VYVUvAy@V]xCsFR[ZYFCL?VDh@D\\AZK`Ak@`A}@ZUVKZGtAGnA@f@APC`@Ib@SXUl@c@bAy@r@i@Z[^e@lAaC\\i@NMVInAQTMPSn@aBh@u@VSVKZ?zBd@X?VGr@_@nAgBjAsAL_@x@kDVaALe@No@@_ABq@Da@Lu@Vk@RYf@a@b@UdGgCz@_APKLKDEd@[`@k@DIx@qAf@kARiAFSFSt@cBLQ^e@TI\\BL{CFo@t@iFFgA?cBCsA[mFBwBLeAjA{Cj@aBTsADq@@i@QeF?k@N{@Rg@V_@^]NKRQXShAeAn@gBZwB\\{DJkB?m@?_AKyBAeCtAeG~AuGd@qA^i@\\o@Vk@Ja@@c@@e@I_Ai@aBEOKe@Oq@CUA[@[BQJo@NWNUd@OPAVBpAv@ZJVBRCTILIb@o@HUP{@@y@Aa@U}@eDoFMWGSKa@O_AMeBUgEFsAJi@Nc@N]X_@rCuCjAcBr@uALk@N_AFwA@]?WC]Eo@eA_FGc@M}@_BcO?_@LUH]BWAs@Q{@m@{A[q@M[a@gAKUWu@IWEQEMIs@KgBAMGqAGqAs@Dc@B[BcAFg@FWHIFOTqAxBKFI@I?QEKCOAa@@k@RGDA?MBQCg@OOE{Ae@_A[k@O}@Yu@GUcAEi@Ca@AW@q@@yA@W?{@IeBK{B?sA?iAJiDGyAOgCGqACw@G_B?k@V_A@WAWOg@k@_ASg@g@eBYgAO}@K{@IuAGcECqC?mDBo@n@iELeBNm@V_@d@w@D]B[Ai@G{@Ig@?e@J{AjAaLd@kDLmA\\wF@y@IaAiA_GSoAOeBIeBA{D@g@?k@Dg@Lq@fAyBDQBkAAi@Aa@j@CjADfAz@d@hA\\bB\\vAVl@VNJH?eFEuH?yBIqCGiCBcAB[Fe@P_AVsAFc@\\cCH{@BYB[?c@AMf@\\l@`@ZTDBf@\\TNl@`@BBj@\\TPVPp@h@rAhA`B~AZ\\T\\T`@PZLPR\\ZXf@L^EbCeBVe@Vw@t@{CP]RSRQlB}@l@On@Fb@XVVbBrBpCrCrCdEFFFLtA~AlB`Dt@p@x@Z?TCj@`BdB|ApB')
    decoded = decode_polyline(geometry)

    print('DECODED:', decoded)
    GeoJson(decoded).add_to(map)

    return map


def get_route_data(cordinates: list[list[float]]):
    assert isinstance(cordinates, list)
    global ors_client

    # sanitize co-ordinates to prevent injection attacks
    # and create co-ordinates in [long, lat] order from
    # [lat, long] order. delete any co-ordinate if it is
    # invalid 
    for co_ordinate in cordinates:
        try:
            lat = float(co_ordinate[0])
            long = float(co_ordinate[1])
            co_ordinate = [long, lat]
        except ValueError:
            del co_ordinate

    # make request and get directions geojson data
    status = 200
    try:
        routes_data = ors_client.directions(cordinates, profile='driving-car') # radiuses=[-1,-1], optimize_waypoints=True
        print('ORG R data:',routes_data)
        routes_data = routes_data.get('routes', [{}])[0]
    except KeyError as e:
        routes_data = {'error':e}
    except ApiError as e:
        routes_data = dict(e.message).get('error', {
            'error': 'try co-ordinates with shorter distance'
        })
        status = 404

    return routes_data, status


def add_markers_to_map(co_ordinates: list[list[float]], map: Map):
    for coordinate in co_ordinates:
        Marker(
            location=coordinate,
            # tooltip='',
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