from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token, get_raw_jwt, get_jwt_identity,
    jwt_optional, jwt_required
)
from marshmallow import ValidationError

from app.extensions import db
from app.models import UserModel
from app.serializers import UserSchema

auth = Blueprint("auth", __name__, url_prefix="/auth")
