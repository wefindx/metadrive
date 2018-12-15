from starlette.applications import Starlette

from starlette.responses import PlainTextResponse
from starlette.responses import JSONResponse
from starlette.websockets import WebSocket
from starlette.graphql import GraphQLApp
from starlette.endpoints import HTTPEndpoint

import uvicorn
import graphene

from urllib import parse

# https://github.com/encode/starlette-example/blob/master/app.py

app = Starlette()
app.debug = True

@app.route('/')
def homepage(request):
    return PlainTextResponse('Hello, world!')

@app.route("/address")
class Address(HTTPEndpoint):

    async def get(self, request):
        address = request.query_params.get('url')
        return JSONResponse({"url": "{}".format(address)})

    async def post(self, request):
        return JSONResponse({"Hello": "POST"})

@app.route('/thing/{this}')
class Thing(HTTPEndpoint):
    async def get(self, request):
        data = request.path_params['this']
        return PlainTextResponse(data)

@app.route('/update')
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

    # for url in wiki_home_urls:
    #     url

    return JSONResponse({'hello': 'world'})

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

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
