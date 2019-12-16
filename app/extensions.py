from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy


blacklist = set()
db = SQLAlchemy()
jwt = JWTManager()
