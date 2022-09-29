import json
from aiohttp.web import Response


def create_json_response(data: dict, status_code: int = 200):
    assert isinstance(status_code, int)
    return Response(text=json.dumps(data), content_type='application/json', status=status_code)


def to_cordinates(location: str, default: tuple[float] = (28.653458, 77.123767)):
    assert isinstance(location, str)

    co_ords = default
    try:
        lat, long = [float(pos) for pos in location.split(',')]
        co_ords = (lat, long) or default
    except ValueError:
        pass

    return co_ords


async def get_json_data(request):
    try:
        if request.headers.get('Content-Type', None):
            data = await request.json()
    except json.decoder.JSONDecodeError:
        data = {'err': 'Invalid JSON format'}
    else:
        data = data or {'msg': 'No JSON data found'}

    return data


def sanitize(data: str) -> str:
    return str(data).replace('\"', '&quot;').replace('\'', '&#39;').replace('<', '&lt;').replace('>', '&gt;')
