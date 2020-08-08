from fplsupercharge.server.container import ApplicationContainer


def create_app():
    """Create and return Flask application."""
    container = ApplicationContainer()

    app = container.app()
    app.container = container

    app.add_url_rule('/', view_func=container.index_view.as_view())

    return app