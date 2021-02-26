from dependency_injector.wiring import inject



@inject
def index():
    return "<h1>Welcome to our server !!</h1>"