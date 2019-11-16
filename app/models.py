from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class DataModel(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(55))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_by = db.relationship("UserModel")
    created_on = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        super(DataModel, self).__init__(**kwargs)
        self.created_on = datetime.utcnow()
