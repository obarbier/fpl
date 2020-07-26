import sys
import os
import shlex
import textwrap
import asyncio

from flask import Flask, session, send_from_directory, Response, request

from fplsupercharge.Utils.process import exec_cmd
from fplsupercharge.server.ServerRequestHandler import _add_static_prefix
from fplsupercharge.protos.apiServices_pb2 import ApiServices, ListTeams, rpc
from fplsupercharge.Utils.protosUtils import message_to_json, parse_dict
from fplsupercharge.Utils.constants import API_BASE_URL
from fplsupercharge.converter.ProtobuffConverter import ProtobuffConverter
from fplsupercharge.FplRequestApiHandler import FplRequestApiHandler

REL_STATIC_DIR = "js/build"
loop = asyncio.get_event_loop()
app = Flask(__name__, static_folder=REL_STATIC_DIR)
STATIC_DIR = os.path.join(app.root_path, REL_STATIC_DIR + "/static")
INDEX_DIR = os.path.join(app.root_path, REL_STATIC_DIR)


def _not_implemented():
    response = Response()
    response.status_code = 404
    return response


def _listTeams():
    fplRequestApiHandler = FplRequestApiHandler()
    
    # response_message = ListTeams.Response()
    # response_message = fplRequestApiHandler.get_teams()
    # response = Response(mimetype='application/json')
    # response.set_data(message_to_json(response_message))
    return response


HANDLERS = {
    # Tracking Server APIs
    ListTeams: _listTeams
}


def _get_paths(base_path):
    """
    A service endpoints base path is typically something like /preview/mlflow/experiment.
    We should register paths like /api/2.0/preview/mlflow/experiment and
    /ajax-api/2.0/preview/mlflow/experiment in the Flask router.
    """
    return ['/api/2.0{}'.format(base_path), _add_static_prefix('/ajax-api/2.0{}'.format(base_path))]


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


for http_path, handler, methods in get_endpoints():
    app.add_url_rule(http_path, handler.__name__, handler, methods=methods)

# CSS/JS resources will be made to /static/index.css and we can handle
# them here.


@app.route(_add_static_prefix('/static/<path:path>'))
def serve_static_file(path):
    return send_from_directory(STATIC_DIR, path)


# Serve the index.html for the React App for all other routes.
@app.route(_add_static_prefix('/'))
def serve():
    if os.path.exists(os.path.join(INDEX_DIR, "index.html")):
        return send_from_directory(INDEX_DIR, 'index.html')

    text = textwrap.dedent('''
    404
    ''')
    return Response(text, mimetype='text/plain')


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
    exec_cmd(full_command, env=env_map, stream_output=True)
