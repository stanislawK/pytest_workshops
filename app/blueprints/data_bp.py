from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError

from app.extensions import db
from app.models import DataModel, UserModel
from app.serializers import DataSchema

data = Blueprint("data", __name__, url_prefix="/data")


@data.route("/", methods=["GET", "POST"])
@jwt_required
def data_get_add():
    user_id = get_jwt_identity()
    user_db = UserModel.query.get_or_404(user_id)
    if request.method == "POST":
        try:
            data_schema = DataSchema().load(request.get_json())
        except ValidationError as err:
            return err.messages, HTTPStatus.BAD_REQUEST
        new_data = DataModel(user_id=user_db.id, **data_schema)
        db.session.add(new_data)
        db.session.commit()
        return jsonify(DataSchema().dump(new_data)), HTTPStatus.CREATED

    data = DataModel.query.all()
    return jsonify(DataSchema(many=True).dump(data)), HTTPStatus.OK
