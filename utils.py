import json
from aiohttp.web import Response, Request


def create_json_response(data: dict, status_code: int = 200):
    '''
    creates json response for web application based on passed params
    '''
    assert isinstance(status_code, int)
    return Response(text=json.dumps(data), content_type='application/json', status=status_code)


def to_cordinates(location: str, default: tuple[float] = (28.653458, 77.123767)):
    '''
    converts string obj to floating co-ordinate numbers
    '''
    assert isinstance(location, str)

    co_ords = default
    try:
        lat, long = [float(pos) for pos in location.split(',')]
        co_ords = (lat, long) or default
    except ValueError:
        pass

    return co_ords


async def get_json_data(request: Request) -> tuple:
    '''
    extracts json data from request and returns data and status code
    '''
    status = 400
    data = None
    try:
        if request.headers.get('Content-Type', None):
            data = await request.json()
            status = 200
    except json.decoder.JSONDecodeError:
        data = {'err': 'Invalid JSON format'}
    else:
        data = data or {'msg': 'No JSON data found'}

    return data, status


def to_sorted_locations_list(locations: list):
    '''
    converts locations list elems to floating numbers then 
    returns sorted list based on location node weight value
    '''
    new_locs = []
    # convert elems to float
    for location in locations:
        try:
            new_locs.append([float(data) for data in location])
        except ValueError:
            pass

    # sort locations based on their node weights
    status = True
    try:
        new_locs = sorted(new_locs, key=lambda location: location[2])
    except Exception:
        status = False

    return new_locs, status


def sanitize(data: str) -> str:
    '''
    replaces html content
    '''
    return str(data).replace('\"', '&quot;').replace('\'', '&#39;').replace('<', '&lt;').replace('>', '&gt;')
