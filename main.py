from sanic import Sanic
from sanic import response
from pynode.node import user_node as user
from pynode.node import loader

app = Sanic()

@app.route("/")
async def homepage(_request):
    return response.json({"hello": "world"})

@app.route("/create")
async def create_user(_request):
    name: str = 'savil'
    twitter_handle: str = 'savils'
    user_node_id = (
        await user.UserNodeMutator()
        .set_name(name)
        .set_twitter_handle(twitter_handle)
        .create()
    )
    user_node = await loader.NodeLoader.load(user_node_id)
    return response.text(f"user node is {vars(user_node)}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
