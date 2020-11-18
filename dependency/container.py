
from logging.config import dictConfig
from dependency_injector import containers, providers

from routers import routers
from . import service

class Log(containers.DeclarativeContainer):

    config = providers.Configuration()

    logging = providers.Resource(
        dictConfig,
        config = config.logging
    )

class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    log = providers.Container(Log , config = config.log) # Initialize log configs

    nano_service = providers.Factory(service.NanoService , config.nano_node.client)
    geo_service = providers.Factory(service.GeoLocationService , db = config.geo_database)
    router_nano = providers.Singleton(routers.NanoNode , nano_service = nano_service , geo_service = geo_service)

    