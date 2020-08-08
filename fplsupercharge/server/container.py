from dependency_injector import containers, providers
from dependency_injector.ext import flask
from flask import Flask
from fplsupercharge.server.handlers import get_endpoints


class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    app = flask.Application(Flask, __name__,
                            static_folder="js/build")
    endpoints = flask.Extension(get_endpoints)
