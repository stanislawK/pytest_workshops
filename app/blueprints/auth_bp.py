from http import HTTPStatus

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.extensions import db
from app.models import UserModel
from app.serializers import UserSchema

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/register/", methods=["post"])
def register():
    # Try to get payload from user and serialize it with marshmallow
    try:
        user_data = UserSchema().load(request.get_json())
    except ValidationError as err:
        return err.messages, HTTPStatus.BAD_REQUEST

    # Check if user with that email exists in db alredy
    if UserModel.query.filter_by(email=user_data["email"]).first():
        # If so return error msg
        return jsonify(
            {"message": "User with that email exists already"}
        ), HTTPStatus.BAD_REQUEST

    # If payload is correct and user doesn't exists in db create new user model
    # instance, and save it
    new_user = UserModel(**user_data)
    db.session.add(new_user)
    db.session.commit()

    # Return newly created user data, and proper statu code
    return jsonify(UserSchema().dump(new_user)), HTTPStatus.CREATED
