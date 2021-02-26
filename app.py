from flask import Flask, request, jsonify
app = Flask(__name__)


<<<<<<< HEAD
#from .containers import Container
from . import views
=======
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"
>>>>>>> c8380942ebe081cd5a73fdfa6798dc0bd5989157

@app.route('/scan/')
def scanFinvizTicker():
    return request.query_string

<<<<<<< HEAD
def create_app() -> Flask:
    #container = Container()
    #container.wire(modules=[views])
    app = Flask(__name__)
    #app.container = container
    app.add_url_rule('/', 'index', views.index)
=======
>>>>>>> c8380942ebe081cd5a73fdfa6798dc0bd5989157


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)


