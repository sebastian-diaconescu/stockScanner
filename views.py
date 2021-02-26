
from flask import request, render_template
from dependency_injector.wiring import inject, Provide

from containers import Container


@inject
def index():
    return "<h1>Welcome to our server !!</h1>"