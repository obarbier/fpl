import sys
# TODO: Logging in acros the whole application
# import  logging
import shlex
import asyncio
import pathlib
from sanic_cors import CORS, cross_origin


from sanic import Sanic
from sanic.response import raw, json
import aiohttp

from fplsupercharge.Utils.process import exec_cmd
from fplsupercharge.protos.apiServices_pb2 import ApiServices, ListTeams, rpc, Team, Teams
from fplsupercharge.Utils.protosUtils import message_to_json, generateColumnDefsFromMessage, parse_dict
from fplsupercharge import FplRequestApiHandler
from fpl import FPL
REL_STATIC_DIR = "js/build"
loop = asyncio.get_event_loop()
PROJECT_ROOT = pathlib.Path(__file__).parent
STATIC_DIR = PROJECT_ROOT / "js/build"
INDEX_DIR = PROJECT_ROOT / "js/build/index.html"
loop = asyncio.get_event_loop()
app = Sanic(__name__)
CORS(app) # FIXME: allowing only api
fFplRequestApiHandler: FplRequestApiHandler


@app.listener('before_server_start')
async def init(app, loop):
    app.aiohttp_session = aiohttp.ClientSession(loop=loop);


@app.listener('after_server_stop')
def finish(app, loop):
    loop.run_until_complete(app.aiohttp_session.close())
    loop.close()


def _not_implemented():
    # response = Response()
    # response.status_code = 404
    # return response
    pass


@app.route("/me")
async def test(request):
    fplRequestApiHandler = FPL(app.aiohttp_session)
    me = await fplRequestApiHandler.get_classic_league(123, return_json=True)
    return json(me)


async def _listTeams(request):
    response_message = ListTeams.Response()
    generateColumnDefsFromMessage(Team, response_message)
    res = response_message.rowData
    fplRequestApiHandler = FPL(app.aiohttp_session)
    teams = await fplRequestApiHandler.get_teams(return_json=True)
    for t in teams:
        team = res.add()
        team = parse_dict(t, team)
    return raw(message_to_json(response_message),status=200 ,headers={ "Content-Type":"application/json"})


HANDLERS = {
    # Tracking Server APIs
    ListTeams: _listTeams
}


def _get_paths(base_path):
    return ['/api/2.0{}'.format(base_path)]


def get_handler(request_class):
    """
    :param request_class: The type of protobuf message
    :return:
    """
    return HANDLERS.get(request_class, _not_implemented)


def get_endpoints():
    """
    :return: List of tuples (path, handler, methods)
    """

    def get_service_endpoints(service):
        ret = []
        for service_method in service.DESCRIPTOR.methods:
            endpoints = service_method.GetOptions(
            ).Extensions[rpc].endpoints
            for endpoint in endpoints:
                for http_path in _get_paths(endpoint.path):
                    handler = get_handler(
                        service().GetRequestClass(service_method))
                    ret.append((http_path, handler, [endpoint.method]))
        return ret

    return get_service_endpoints(ApiServices)


# setup views and routes
for http_path, handler, methods in get_endpoints():
    app.add_route(uri=http_path, handler=handler,
                  name=handler.__name__, methods=methods)


def _build_waitress_command(waitress_opts, host, port):
    opts = shlex.split(waitress_opts) if waitress_opts else []
    return ['waitress-serve'] + \
        opts + [
        "--host=%s" % host,
        "--port=%s" % port,
        "--ident=fplsupercharge",
        "fplsupercharge.server:app"
    ]


def _build_gunicorn_command(gunicorn_opts, host, port, workers):
    bind_address = "%s:%s" % (host, port)
    opts = shlex.split(gunicorn_opts) if gunicorn_opts else []
    return ["gunicorn"] + \
        opts + [
            "-b",
            bind_address,
            "-w",
            "%s" % workers,
            "--worker-class",
            "sanic.worker.GunicornWorker",
            "fplsupercharge.server:app"]


def _run_server(host, port, opts):
    """
    :return: None
    """
    env_map = {}
    if sys.platform == 'win32':
        full_command = _build_waitress_command(opts, host, port)
    else:
        full_command = _build_gunicorn_command(opts, host, port, 4)
    exec_cmd(full_command, env=env_map, stream_output=True)
