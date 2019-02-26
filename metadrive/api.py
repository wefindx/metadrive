import os
import yaml
import uvicorn
import inspect
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
        'id': '{scheme}://{host}{port}/driver/{name}'.format(
            scheme=request.url.scheme,
            host=request.client.host,
            port=(request.url.port not in [80,443]
                  and ':'+str(request.url.port) or ''),
            name=driver[1].split('==')[0]),
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

        ndriver = driver.replace('-', '_')

        module = __import__(ndriver)
        api = __import__('{}.api'.format(ndriver), fromlist=[ndriver])

        core = inspect.getmembers(module)
        api = inspect.getmembers(api)

        try:
            auth = {
                item[0]: inspect.getcallargs(item[1]) for item in core
                if item[0].startswith('_') and
                not item[0].startswith('__')}
        except Exception as e:
            auth = {}

        try:
            types = {
                item[0]: {
                    method[0]: str(inspect.signature(method[1]))
                    for method in inspect.getmembers(
                        item[1], predicate=inspect.ismethod)}
                for item in api
                if repr(item[-1]).startswith(
                "<class '{}.api.".format(ndriver))}
        except Exception as e:
            types = {}


        schema = {
            'driver': driver,
            'auth': auth,
            'types': types
        }
         # will depend on package!

        return JSONResponse(schema)


@app.route("/drive/{name}/{method}")
class Drive(HTTPEndpoint):
    async def post(self, request):
        """
        summary: /drive/{name}/{method}
        description: |
            Calls driver's methods with parameters.
            If method is part of class, then it has '.'

            Example:
            requests.post(url, params={'a': 'data'}, json={'some': 'data'})
        """

        driver = request.path_params['name']
        ndriver = driver.replace('-', '_')
        method = request.path_params['method']
        params = request.query_params

        if '.' in method:
            classname, method = method.split('.', 1)
        else:
            classname, method = None, method

        try:
            payload = await request.json()
        except:
            payload = None

        drive_instance = params.get('drive_id')

        if drive_instance is None and classname is not None:
            return JSONResponse({
                "drive_id": "Missing URL argument. To get drive_id, use _login() method"
            })


        if classname is None and method in ['_login']:
            package = __import__(ndriver)
            driver = getattr(package, '_login')()
            print('hello, the driver was created')
            print(dir(driver))
        else:
            print('oops')
            print(classname, method)

        #
        # if classname is not None:
        #     Klass = __import__(classname, fromlist=[ndriver, 'api'])
        #
        #     if method:
        #         getattr(Klass, method)(driver=instance)


        return JSONResponse({
            'driver': str(repr(driver)),
            'type': classname,
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
