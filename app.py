from flask import Flask, request, jsonify
app = Flask(__name__)

<<<<<<< HEAD

@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
=======
from flask import Flask
from flask_bootstrap import Bootstrap
from flask import request, render_template
from dependency_injector.wiring import inject, Provide

from containers import Container


@inject
def index():
    return "<h1>Welcome to our server !!</h1>"

def create_app() -> Flask:
    container = Container()    
    container.wire(modules=[views])
    app = Flask(__name__)
    app.container = container
    app.add_url_rule('/', 'index', views.index)

    bootstrap = Bootstrap()
    bootstrap.init_app(app)

    return app
>>>>>>> 119ca400c34a53a9defac0a0e21b964d1dff0b0c
