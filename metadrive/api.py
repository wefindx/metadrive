from starlette.applications import Starlette
from starlette.responses import JSONResponse
import uvicorn

from starlette.graphql import GraphQLApp
import graphene


class Query(graphene.ObjectType):
    hello = graphene.String(
        name=graphene.String(
            default_value="stranger"))

    def resolve_hello(self, info, name):
        return "Hello " + name

app = Starlette()
app.add_route('/', GraphQLApp(
    schema=graphene.Schema(
        query=Query)))

@app.route('/hi')
async def homepage(request):
    return JSONResponse({'hello': 'world'})

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
