import os
from fplsupercharge.container import ApplicationContainer
from flask import send_from_directory, g
from flask_cors import CORS


def create_ui():
    """Create and return Flask application."""
    # initiate app
    REL_STATIC_DIR = 'js/build'
    container = ApplicationContainer()
    app = container.app()
    CORS(app) #TODO: Do we really needs CORS
    app.container = container
    # static file setup
    STATIC_DIR = os.path.join(app.root_path, REL_STATIC_DIR)
    @app.before_request
    def init_db():
        g.db = container.db()
    with app.app_context():
        # setup views and routes
        @app.route("/health")
        def health():  # Health check endpoint
            return "OK", 200

        @app.route('/static/<path:path>')
        def serve_static_file(path):
            return send_from_directory(STATIC_DIR + "/static", path)

        @app.route('/')
        def serve():
            if os.path.exists(os.path.join(STATIC_DIR, "index.html")):
                return send_from_directory(STATIC_DIR, 'index.html')

        for http_path, handler, methods in container.endpoints():
            app.add_url_rule(http_path, handler.__name__, handler,
                             methods=methods)
    return app
