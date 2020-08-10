"""Console script for fplsupercharge."""


import sys
import click
import os
import shutil
import configparser

from fplsupercharge.container import (Waitress,
                                      Gunicorn,
                                      RunServer,
                                      Core)
from fplsupercharge.utils import coroutine , cli_args, iniFileConstant
import logging.config

# setting
logging.config.fileConfig('logging.conf')
core = Core()
logger = core.logger().getChild("cli")
@click.group()
@click.version_option()
def main(args=None):
    pass


@main.command()
@cli_args.USERNAME
@cli_args.PASSWORD
@cli_args.INITYPE
@cli_args.REFRESH_DATA
@cli_args.DBTYPE
@cli_args.DATABASEURL
@cli_args.DATABASEPASSWORD
def init(username, password, initype, refresh, dbtype, dburl, dbpass):
    """User metada to be save
    : params
    USERNAME     : Username need to Login to FPL
    PASSWORD     : Password need to Login to FPL
    INITYPE     : where to save data
    REFRESH_DATA : how often we will update record
    databaseType: persistence database type
    databaseUri: persistant datapase URL"""
    if click.confirm('Do you want to continue?', default=True):
        try:
            os.mkdir(iniFileConstant.TEMP_FILE_DIR)
        except OSError:
            print(iniFileConstant.TEMP_CREATION_MESSAGE_FAILED)
        else:
            # FIXME:Test if file is present
            config = configparser.ConfigParser()
            # FIXME: VERIFY data_provide
            config.add_section(iniFileConstant.SECTION.get(1))
            config.set(iniFileConstant.SECTION.get(1), 'username', username)
            config.set(iniFileConstant.SECTION.get(1), 'password', password)
            config.set(iniFileConstant.SECTION.get(1), 'initype', initype)
            config.set(iniFileConstant.SECTION.get(
                1), 'refresh', refresh)
            config.set(iniFileConstant.SECTION.get(1), 'dbtype', dbtype)
            config.set(iniFileConstant.SECTION.get(
                1), 'dburl', dburl)
            config.set(iniFileConstant.SECTION.get(
                1), 'dbpass', dbpass)
            with open(iniFileConstant.SAVE_TEMPLATE.format(
                    iniFileConstant.FILE_NAME), 'w') as configfile:
                config.write(configfile)
            # FIXME: ENCODE/ENCRYPT using key
            print(iniFileConstant.INI_CREATION_MESSAGE_SUCCESS)


@main.command()
def teardown():
    """graceful way to delete all metadata store"""
    # FIXME: Gracefully handle deletion of files
    if click.confirm('Do you want to delete all data file?'):
        try:
            shutil.rmtree(iniFileConstant.TEMP_FILE_DIR)
        except Exception:
            print(iniFileConstant.TEMP_DELETE_MESSAGE_FAILED)
        else:
            print(iniFileConstant.TEMP_DELETE_MESSAGE_SUCCESS)


@main.command()
@cli_args.PORT
@cli_args.HOST
# FIXME: Application need to get perisistence info from initFile
def ui(port, host):
    if sys.platform == 'win32':
        adapters = Waitress()
    else:
        adapters = Gunicorn()
    RunServer.run(cmd=adapters.server())


@main.command()
@coroutine
async def initializedb():
    try:
        await RunServer.intialDataLoad()
    except Exception as ex:
        logger.error(ex)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
