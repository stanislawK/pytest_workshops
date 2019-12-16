from pathlib import Path

from flask import Flask

from app.blueprints.auth_bp import auth
from app.blueprints.data_bp import data
from app.extensions import blacklist, db, jwt


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        r'sqlite:///{}'.format(Path('app/test.db').absolute())
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'secret'
    app.config['JWT_BLACKLIST_ENABLED'] = True

    db.init_app(app)
    jwt.init_app(app)
    app.register_blueprint(auth)
    app.register_blueprint(data)

    return app


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token["jti"]
    return jti in blacklist
