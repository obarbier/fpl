import sys
import os
import shlex
import textwrap

from flask import Flask, send_from_directory, Response

from fpl.Utils.process import exec_cmd
from fpl.server.ServerRequestHandler import STATIC_PREFIX_ENV_VAR, _add_static_prefix

REL_STATIC_DIR = "js/build"
app = Flask(__name__, static_folder=REL_STATIC_DIR)
STATIC_DIR = os.path.join(app.root_path, REL_STATIC_DIR + "/static")
INDEX_DIR = os.path.join(app.root_path, REL_STATIC_DIR)


# CSS/JS resources will be made to e.g. /static/index.css and we can handle them here.
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
               "--ident=fpl",
               "fpl.server:app"
           ]


def _build_gunicorn_command(gunicorn_opts, host, port, workers):
    bind_address = "%s:%s" % (host, port)
    opts = shlex.split(gunicorn_opts) if gunicorn_opts else []
    return ["gunicorn"] + opts + ["-b", bind_address, "-w", "%s" % workers, "fpl.server:app"]


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
