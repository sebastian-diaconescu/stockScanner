"""Application module."""

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