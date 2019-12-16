from pathlib import Path

from flask import Flask

from app.blueprints.auth_bp import auth
from app.blueprints.data_bp import data
from app.extensions import db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        r'sqlite:///{}'.format(Path('app/test.db').absolute())
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.register_blueprint(auth)
    app.register_blueprint(data)

    return app
