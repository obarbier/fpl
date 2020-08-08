import logging
from dependency_injector import containers, providers

from fplsupercharge.server import utils


class Core(containers.DeclarativeContainer):
    """IoC container of core component providers."""

    config = providers.Configuration('config')
    # TODO: Logging in acros the whole application
    # logger = providers.Singleton(logging.Logger, name='example')


class Waitress(containers.DeclarativeContainer):
    """Adapters container."""
    server = providers.Callable(utils.build_waitress_command)


class Gunicorn(containers.DeclarativeContainer):
    """Adapters container."""
    # FIXME
    server = providers.Callable(utils.build_gunicorn_command,
                                opts=None,
                                host='0.0.0.0',
                                port=5050,
                                workers=4)


class RunServer(containers.DeclarativeContainer):
    run = providers.Callable(utils.exec_cmd)
