import os
import yaml
import uvicorn
import inspect
import graphene
import collections
from urllib import parse
import pkg_resources

from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.responses import JSONResponse
from starlette.websockets import WebSocket
from starlette.graphql import GraphQLApp
from starlette.endpoints import HTTPEndpoint
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from starlette.schemas import (
    SchemaGenerator,
    OpenAPIResponse
)

from metadrive.config import (
    INSTALLED,
    API_HOST,
    API_PORT,
    DATA_DIR,
)
from metadrive.cli import (
    FILENAME_LENGTH_LIMIT
)
from metadrive.utils import find_drivers
from metadrive import drives as mdrives
from typology.utils import slug

import metaform
import metawiki


app = Starlette(template_directory=os.path.join(INSTALLED, '_api_templates'))
app.add_middleware(CORSMiddleware, allow_origins=['*'])
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
''', Loader=yaml.FullLoader)


DEFAULT_MAX_COUNT = 20
PAGE_SIZE = 10
DATA_PATH = None
DATA_FOLDER = None


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
            host=API_HOST,
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
        description: Provides description of driver's methods
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

            if '_login' in auth.keys():
                if 'create' not in auth['_login'].keys():
                    auth['_login'].update({'create': True})

            auth.update({
                '_logout': {
                    'destroy': True
                },
                '_start': "()",
                '_stop': "()",
                '_restart': "()",
                '_remove': "()",
            })
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


        info = {
            'driver': driver,
            'auth': auth,
            'types': types
        }

        return JSONResponse(info)


@app.route('/drives')
async def drives(request):
    '''
    summary: /drives
    description: Lists the drives available in API.
    responses:
      200:
        description: A list of drives.
    '''

    items = [
        v
        for k, v in enumerate(mdrives.all())
    ]

    return JSONResponse(items)


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
        ndriver = driver.split(':', 1)[0].replace('-', '_')
        method = request.path_params['method']
        params = request.query_params
        drive_id = driver.split(':', 1)[1]
        version = pkg_resources.require(ndriver)[0].version

        if os.name in ['nt']:
            DATA_FOLDER = os.path.join(DATA_DIR, driver.replace(':', '__'))
        else:
            DATA_FOLDER = os.path.join(DATA_DIR, driver)

        if not os.path.exists(DATA_FOLDER):
            os.makedirs(DATA_FOLDER)

        results_count = params.get('count')
        schema = params.get('schema')
        template = params.get('template')
        refresh = params.get('refresh')
        formatize = params.get('formatize')

        if isinstance(schema, str):
            schema_url = metawiki.ext2url(schema)
            if refresh is not None:
                schema = metaform.get_schema(schema_url, refresh=True)
            else:
                schema = metaform.get_schema(schema_url)
        else:
            schema_url = None

        template_format = 'json'
        if template in ['json', 'dict', 'yaml']:
            template_format = template


        if '.' in method:
            classname, method = method.split('.', 1)
        else:
            classname, method = None, method

        if os.name in ['nt']:
            DATA_PATH = os.path.join(DATA_DIR, driver.replace(':', '__'), classname)
        else:
            DATA_PATH = os.path.join(DATA_DIR, driver, classname)

        if not os.path.exists(DATA_PATH):
            os.makedirs(DATA_PATH)

        try:
            payload = await request.json()
        except:
            payload = {}

        parameters = payload

        if results_count is not None:
            results_count = int(results_count)

        drive_obj = mdrives.get(driver)

        if method in ['_login']:

            package = __import__(ndriver)
            drive_obj = getattr(package, method)(drive=drive_obj) # create=False to avoid _start

            return JSONResponse({
                'info': "Drive created. Use it with other methods.",
                'driver': drive_obj.drive_id.split(':')[0],
                'drive_id': drive_obj.drive_id.split(':')[-1],
            })

        if method in ['_start']:
            if drive_obj is None:
                package = __import__(ndriver)
                drive_obj = getattr(package, '_login')(drive=None)


        if method in ['_stop']:
            stopping_driver = drive_obj.drive_id.split(':')[0]
            stopping_drive = drive_obj.drive_id.split(':')[-1]

            mdrives.close(drive_obj)
            drive_obj = None


            return JSONResponse({
                'info': 'Drive stopped.',
                'drive': '{}:{}'.format(
                    stopping_driver,
                    stopping_drive,
                )
            })

        if method in ['_restart']:

            restarting_driver = drive_obj.drive_id.split(':')[0]
            restarting_drive = drive_obj.drive_id.split(':')[-1]

            mdrives.close(drive_obj)

            package = __import__(ndriver)
            drive_obj = getattr(package, '_login')(drive=None)

            return JSONResponse({
                'info': 'Drive restarted.',
                'drive': '{}:{}'.format(
                    restarting_driver,
                    restarting_drive,
                )
            })

        if method in ['_remove']:
            stopping_driver = drive_obj.drive_id.split(':')[0]
            stopping_drive = drive_obj.drive_id.split(':')[-1]

            mdrives.remove(drive_obj)
            drive_obj = None

            return JSONResponse({
                'info': 'Drive removed.',
                'drive': '{}:{}'.format(
                    stopping_driver,
                    stopping_drive,
                )
            })


        if drive_obj is not None:

            parameters = dict({'drive': drive_obj}, **parameters)


            if classname is not None:

                module = __import__(ndriver)
                api = __import__('{}.api'.format(ndriver), fromlist=[ndriver])
                Klass = getattr(api, classname)

                if method is not None:

                    available_parameters = {}
                    for key in parameters:
                        if key in getattr(Klass, method).__code__.co_varnames:
                            available_parameters.update({key: parameters[key]})


                    # _get #
                    if method in ['_get']:

                        try:
                            result = getattr(Klass, method)(**available_parameters)
                        except:
                            raise Exception("Could not call method. Maybe not implemented?")

                        # return if asks for template
                        if template is not None:

                            if template == 'yaml':
                                return PlainTextResponse(
                                    yaml.dump(metaform.metaplate(result, ret=True), default_flow_style=False)
                                )

                            return JSONResponse(
                                metaform.metaplate(result, ret=True)
                            )

                        # normalization
                        if schema_url:
                            result = metaform.normalize(result, schema=schema)
                            result['*'] = schema_url

                        return JSONResponse({
                            'result': result,
                            'path': '{scheme}://{host}{port}{path}'.format(
                                scheme=request.url.scheme,
                                host=API_HOST,
                                port=(request.url.port not in [80,443]
                                      and ':'+str(request.url.port) or ''),
                                path=request['path']
                            ),
                        })


                    # _filter #

                    if method in ['_filter']:

                        if not hasattr(drive_obj, 'generator'):

                            try:
                                result = getattr(Klass, method)(**available_parameters)
                            except:
                                raise Exception("Could not call method. Maybe not implemented?")

                            drive_obj.generator = {
                                'name': '{}.{}'.format(classname, method),
                                'iterator': result
                            }
                        elif drive_obj.generator.get('name') != '{}.{}'.format(classname, method):
                            result = getattr(Klass, method)(**available_parameters)

                            drive_obj.generator = {
                                'name': '{}.{}'.format(classname, method),
                                'iterator': result
                            }


                        results = []

                        if hasattr(drive_obj, 'generator'):
                            if drive_obj.generator.get('iterator'):
                                for i in range(PAGE_SIZE):

                                    item = next(drive_obj.generator['iterator'])

                                    if (not hasattr(item, '_drive')) or (item._drive is None):


                                        # TODO: refactor with drives.py#creating-informative-drive

                                        # creating-informative-drive #
                                        item._drive = '{packman}::{driver}=={version}:{profile}.{namespace}'.format(
                                            packman='PyPI',
                                            driver=drive_obj.drive_id.split(':',1)[0],
                                            version=version,
                                            profile=drive_obj.drive_id.rsplit(':',1)[-1],
                                            namespace='{}.{}'.format(
                                                item.__class__.__dict__['__module__'].split('.',1)[-1],
                                                item.__class__.__name__,
                                            )
                                        )

                                        item['@'] = item._drive

                                    if schema_url:
                                        item['*'] = schema_url

                                    results.append(item)
                                    item.save()

                        if template is not None:

                            if template == 'yaml':
                                return PlainTextResponse(
                                    yaml.dump(metaform.metaplate(results, ret=True)[0], default_flow_style=False)
                                )

                            return JSONResponse(
                                metaform.metaplate(results, _format=template_format, ret=True)[0]
                            )

                        # normalization
                        if schema_url:
                            results = metaform.normalize(results, schema=[schema])

                        return JSONResponse({
                            'results': results,
                            'count': results_count or DEFAULT_MAX_COUNT,
                            'next': '{scheme}://{host}{port}{path}'.format(
                                scheme=request.url.scheme,
                                host=API_HOST,
                                port=(request.url.port not in [80,443]
                                      and ':'+str(request.url.port) or ''),
                                path=request['path']
                            ),
                        })


        return JSONResponse({
            'driver': str(repr(driver.split(':', 1)[0])),
            'type': classname,
            'method': method,
            'params': dict(params),
            'payload': payload,
            # 'drives': str(drives.ACTIVE),
        })


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
    uvicorn.run(app, host=API_HOST, port=API_PORT)
