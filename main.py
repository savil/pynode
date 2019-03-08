from sanic import Sanic
from sanic.response import json
from pynode.node.user_node import UserNodeMutator

app = Sanic()

@app.route("/")
async def homepage(request):
    return json({"hello": "world"})

@app.route("/create")
async def create_user(request):
    name: str = 'savil'
    twitter_handle: str = 'savils'
    user_node = await UserNodeMutator().set_name(name).set_twitter_handle(twitter_handle).create()
    return repr(user_node)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
