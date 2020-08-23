# core module
import logging
import aiohttp
# third-party modules
from dependency_injector import containers, providers
from dependency_injector.ext import flask
from flask import Flask
import kaptan

# application module
from fplsupercharge.utils.flaskHandlers import get_endpoints
from fplsupercharge.utils.serverHandler import (build_gunicorn_command,
                                                build_waitress_command,
                                                exec_cmd)
from fplsupercharge.services.neo4jServices import Datastore
from fplsupercharge.services.fplRequestApiServices import FplRequestApiHandler
from fplsupercharge.applications.datastore import intialDataload


class Core(containers.DeclarativeContainer):
    """IoC container of core component providers."""
    kp = kaptan.Kaptan(handler="ini")
    kp.import_config('../tmp/FPLSUPERCHARGE.ini')
    config = providers.Factory(kp.get)
    logger = providers.Singleton(logging.getLogger)
    fplSessionManager = providers.Singleton(aiohttp.ClientSession)


class Waitress(containers.DeclarativeContainer):
    """Adapters container."""
    server = providers.Callable(build_waitress_command,
                                logger=Core.logger,)


class Gunicorn(containers.DeclarativeContainer):
    """Adapters container."""
    # TODO: DYNAMIC PORT based on config
    server = providers.Callable(build_gunicorn_command,
                                logger=Core.logger,
                                opts=None,
                                host='0.0.0.0',
                                port=5050,
                                workers=4)


class Services(containers.DeclarativeContainer):
    """IoC container for all services."""
    neo4jServices = providers.Singleton(Datastore,
                                        uri=Core.config(
                                            key="init.dburl"),
                                        username=Core.config(
                                            key="init.dbname"),
                                        password=Core.config(
                                            key="init.dbpass"),
                                        logger=Core.logger(name="neo4jServices"))

    fplRequestApiServices = providers.Factory(FplRequestApiHandler,
                                              session=Core.fplSessionManager)


class ApplicationContainer(containers.DeclarativeContainer):
    app = flask.Application(Flask, __name__,
                            static_folder="js/build")
    db = flask.Extension(Services.neo4jServices)
    logger = flask.Extension(Core.logger)
    endpoints = flask.Extension(get_endpoints)


class GRPCApplicationConTainer(containers.DeclarativeContainer):
    # TODO: Transform to using GRPC
    pass


class RunServer(containers.DeclarativeContainer):
    run = providers.Callable(exec_cmd,
                             logger=Core.logger)
    intialDataLoad = providers.Callable(intialDataload,
                                        username=Core.config(
                                            key="init.username"),
                                        password=Core.config(
                                            key="init.password"),
                                        logger=Core.logger,
                                        db=Services.neo4jServices,
                                        fplRequestApiServices=Services
                                        .fplRequestApiServices
                                        )
