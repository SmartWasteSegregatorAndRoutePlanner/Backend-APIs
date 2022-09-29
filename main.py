from aiohttp import web
from views import Maps
from utils import create_json_response

import logging
logging.basicConfig(level=logging.DEBUG)

async def home(request):
    response = {'msg':'working'}
    return create_json_response(response)

# create web application
app = web.Application()

# routes
app.router.add_get('/', home)
app.router.add_view('/api/maps', Maps)


if __name__ == '__main__':
    web.run_app(
        app=app, 
        host='0.0.0.0',
        port=8080,
    )
