from aiohttp import web
from aiohttp_swagger import setup_swagger
from os import environ
from utils import create_json_response
from views import Maps

import logging
logging.basicConfig(level=logging.DEBUG)


async def home(request):
    response = {'msg': 'working'}
    return create_json_response(response)

# create web application
app = web.Application()

# routes
app.router.add_get('/', home)
app.router.add_view('/api/maps', Maps)

# configure swagger after adding routes
long_description = """
Endpoints used to interact with various components of the project
"""
setup_swagger(
    app=app,
    ui_version=3,
    title='Smart Waste Segregator and Route Planner API',
    description=long_description,
    api_version='1.0.0',
    swagger_url='/api/doc',
    swagger_validator_url='//online.swagger.io/validator',
)

if __name__ == '__main__':
    web.run_app(
        app=app,
        host='0.0.0.0',
        port=environ.get('PORT', 8080),
    )
