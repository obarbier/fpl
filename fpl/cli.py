import json
import os
import sys
import logging

import click

from fpl.server import _run_server
from fpl.Utils import cli_args
from fpl.Utils.process import ShellCommandException

_logger = logging.getLogger(__name__)


@click.group()
@click.version_option()
def cli():
    pass


@cli_args.PORT
@cli_args.HOST
def ui(port, host):
    try:
        _run_server(host, port, None)
    except ShellCommandException:
        print("Running the fpl server failed. Please see the logs above for details.")
        sys.exit(1)


if __name__ == '__main__':
    ui("8080", "0.0.0.0")
