from dependency_injector import containers, providers

from . import services

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    #add members here
