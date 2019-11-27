from flask import Blueprint, jsonify


auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/register/", methods=["post"])
def register():
    pass
