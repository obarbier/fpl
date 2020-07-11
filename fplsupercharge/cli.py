"""Console script for fplsupercharge."""
import sys
import click
import json
import os
import sys
import logging


from fplsupercharge.server import _run_server
from fplsupercharge.Utils import cli_args
from fplsupercharge.Utils.process import ShellCommandException

_logger = logging.getLogger(__name__)


@click.group()
@click.version_option()
def main(args=None):
    pass

@main.command()
@cli_args.PORT
@cli_args.HOST
def ui(port, host):
    try:
        _run_server(host, port, None)
    except ShellCommandException:
        print("Running the fpl server failed. Please see the logs above for details.")
        sys.exit(1)
if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover