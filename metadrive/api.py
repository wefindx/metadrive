from starlette.applications import Starlette

from starlette.responses import PlainTextResponse
from starlette.responses import JSONResponse
from starlette.websockets import WebSocket
from starlette.graphql import GraphQLApp

import uvicorn
import graphene

# https://github.com/encode/starlette-example/blob/master/app.py

app = Starlette()
app.debug = True

@app.route('/')
def homepage(request):
    return PlainTextResponse('Hello, world!')

@app.route('/data')
async def homepage(request):
    return JSONResponse({'hello': 'world'})

@app.websocket_route('/ws')
async def websocket_endpoint(websocket):
    await websocket.accept()
    await websocket.send_text('Hello, websocket!')
    await websocket.close()

@app.on_event('startup')
def startup():
    print('Ready to go')

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
    uvicorn.run(app, host='0.0.0.0', port=7000)
