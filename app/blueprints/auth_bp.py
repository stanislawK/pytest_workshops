from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token, get_raw_jwt, get_jwt_identity,
    jwt_optional, jwt_required
)
from marshmallow import ValidationError

from app.extensions import blacklist, db
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


@auth.route("/login/", methods=["post"])
@jwt_optional
def login():
    # Check if user is logged in already
    current_user = get_jwt_identity()
    if current_user:
        return jsonify(
            {"message": "User logged in already"}
        ), HTTPStatus.UNAUTHORIZED

    # Try to get payload from user and serialize it with marshmallow
    try:
        user_data = UserSchema().load(request.get_json())
    except ValidationError as err:
        return err.messages, HTTPStatus.BAD_REQUEST

    # Look for user with given email in db and check password
    user_db = UserModel.query.filter_by(email=user_data["email"]).first()
    if user_db and user_db.check_password(user_data["password"]):
        token = create_access_token(identity=user_db.id)
        return jsonify({"access_token": token}), HTTPStatus.OK

    return jsonify(
        {"message": "Invalid email or password"}
    ), HTTPStatus.UNAUTHORIZED


@auth.route("/logout/", methods=["delete"])
@jwt_required
def logout():
    jti = get_raw_jwt()["jti"]
    blacklist.add(jti)
    return jsonify({"message": "Successfully logged out"}), HTTPStatus.OK
