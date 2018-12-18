from starlette.applications import Starlette

from starlette.responses import PlainTextResponse
from starlette.responses import JSONResponse
from starlette.websockets import WebSocket
from starlette.graphql import GraphQLApp
from starlette.endpoints import HTTPEndpoint
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

import uvicorn
import graphene

from urllib import parse

import os
from metadrive.config import INSTALLED

# https://github.com/encode/starlette-example/blob/master/app.py

app = Starlette(template_directory=os.path.join(INSTALLED, '_api_templates'))
app.mount('/static', StaticFiles(directory=os.path.join(INSTALLED, '_api_static')), name='static')
app.debug = True

@app.route('/')
def homepage(request):
    return PlainTextResponse('Welcome to MetaDrive!')


@app.route("/address")
class Address(HTTPEndpoint):

    async def get(self, request):
        address = request.query_params.get('url')
        return JSONResponse({"url": "{}".format(address)})

    async def post(self, request):
        return JSONResponse({"Hello": "POST"})

@app.route('/websites')
async def reindex(request):
    '''
        Returns a list of all sites available via
        __site_url__, prepared by reindex()
    '''

    return JSONResponse({'data': 'list-of-websites-availabe-via-__site_url__'})

@app.route('/reindex')
async def reindex(request):
    ''' Goes through all wikis, and all concept pages,
        and through all latest libraries, to see, what
        __site_url__ are available.
    '''
    wiki_home_urls = [
        'https://github.com/mindey/-/wiki',
        'https://github.com/wefindx/-/wiki',
        'https://github.com/DimensionFoundation/-/wiki',
    ]

    # sites_available = []
    # for url in wiki_home_urls:
    #     for page in get_all_pages(url):
    #         for schema in get_schemas(page):
    #             pkg_fun = schema.get('_:emitter')
    #             for file in get_pypi_package(pkg_fun):
    #                 sites_available.append({'site': get_site_url(file), 'emitter': pkg_fun})
    return JSONResponse({'data': 'note about indexing job started, and job id, e.g., celery job id'})

@app.route('/thing/{this}')
class Thing(HTTPEndpoint):
    async def get(self, request):
        data = request.path_params['this']
        return PlainTextResponse(data)

@app.websocket_route('/ws')
async def websocket_endpoint(websocket):
    await websocket.accept()
    await websocket.send_text('Hello, websocket!')
    await websocket.close()

@app.on_event('startup')
def startup():
    pass
    # print('ready')

class Query(graphene.ObjectType):
    hello = graphene.String(
        name=graphene.String(
            default_value="stranger"))

    def resolve_hello(self, info, name):
        return "Hello " + name

app.add_route('/gq', GraphQLApp(
    schema=graphene.Schema(
        query=Query)))

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

@app.route('/index')
async def index(request):
    template = app.get_template('index.html')
    content = template.render(request=request)
    return HTMLResponse(content)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
