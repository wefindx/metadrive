import os
import yaml
import uvicorn
import graphene
from urllib import parse

from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.responses import JSONResponse
from starlette.websockets import WebSocket
from starlette.graphql import GraphQLApp
from starlette.endpoints import HTTPEndpoint
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.schemas import (
    SchemaGenerator,
    OpenAPIResponse
)

from metadrive.config import INSTALLED
from metadrive.utils import find_drivers


app = Starlette(template_directory=os.path.join(INSTALLED, '_api_templates'))
app.mount('/static', StaticFiles(directory=os.path.join(INSTALLED, '_api_static')), name='static')
app.debug = True
app.schema_generator = SchemaGenerator(
    {"swagger": "2.0",
     "info": {
         "title": "MetaDrive API",
         "version": "0.0.1"}})

definitions = yaml.load('''
definitions:
  DriverItem:
    properties:
      site: {format: utf8, type: string}
      package: {format: utf8, type: string}
    type: object
''')

# -------------------------------------------- #

@app.route('/drivers')
async def drivers(request):
    '''
    summary: /drivers
    description: Lists the drivers available in API.
    responses:
      200:
        description: A list of drivers.
        schema:
          '$ref': '#/definitions/DriverItem'
    '''
    drivers = find_drivers()

    items = [{
        'site': driver[0],
        'package': driver[1]}
        for driver in drivers]

    return JSONResponse(items)

@app.route("/driver/{name}")
class Driver(HTTPEndpoint):
    async def get(self, request):
        '''
        summary: /driver/{name}/
        description: Provides description (schema) of driver's methods
        '''
        driver = request.path_params['name']
        params = request.query_params

        schema = {
            'methods': {
                'auth': {},
                'generators': {
                },
            }
        }
         # will depend on package!

        return JSONResponse({
            'driver': driver,
            'schema': schema,
            'params': dict(params),
        })


@app.route("/drive/{name}/{method}")
class Drive(HTTPEndpoint):
    async def post(self, request):
        '''
        summary: /drive/{name}/{method}
        description: Calls driver's methods with parameters.
        '''
        driver = request.path_params['name']
        method = request.path_params['method']
        params = request.query_params
        payload = await request.json()

        return JSONResponse({
            'driver': driver,
            'method': method,
            'params': dict(params),
            'payload': payload
        })

# -------------------------------------------- #

@app.exception_handler(404)
async def not_found(request, exc):
    """
    Return an HTTP 404 page.
    """
    template = app.get_template('404.html')
    content = template.render(request=request)
    return HTMLResponse(content, status_code=404)

@app.exception_handler(500)
async def server_error(request, exc):
    """
    Return an HTTP 500 page.
    """
    template = app.get_template('500.html')
    content = template.render(request=request)
    return HTMLResponse(content, status_code=500)

@app.route('/', include_in_schema=False)
async def index(request):
    template = app.get_template('docs.html')
    content = template.render(request=request)
    return HTMLResponse(content)

@app.route("/schema", include_in_schema=False)
def schema(request):
    return OpenAPIResponse(
        dict(app.schema, **definitions))

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
