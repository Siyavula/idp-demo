import os

from flask import Flask
from app.utils import ensure_client_exists


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SERVER_URL="http://keycloak:7080",
        ADMIN_USERNAME="admin",
        ADMIN_PASS="admin",
        REALM_NAME="master",
        CLIENT_ID="app",
        CLIENT_SECRET="7g7i57WGExptcr28CNhmoR3oWZVzLZLs",
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import auth, home
    app.register_blueprint(home.bp)
    app.register_blueprint(auth.bp)

    # Ensure Keycloak Opend ID Connect client exists
    # You probably wouldn't want do this in production, but it's useful for the demo setup.
    with app.app_context():
        ensure_client_exists()

    return app
