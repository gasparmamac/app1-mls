import os
from flask import Flask


def create_app(test_config=None):
    # create app
    app = Flask(__name__, instance_relative_config=True)

    # configuration setup
    app.config.from_mapping(
        SECRET_KEY='dev',
        # sqlalchemy
        SQLALCHEMY_DATABASE_URI=os.path.join(f"sqlite:////{app.instance_path}", 'mls.db'),
        SQLALCHEMY_ECHO=False,
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    if test_config is None:
        # load the instance config
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # create instance folder
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # initialize extensions
    from .model import db
    from .auth import login_manager
    db.init_app(app)
    login_manager.init_app(app)

    # register blueprints
    from . import auth
    app.register_blueprint(auth.auth_bp)

    with app.app_context():
        db.create_all()

    return app
