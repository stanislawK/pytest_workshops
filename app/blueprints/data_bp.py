from flask import Blueprint


data = Blueprint("data", __name__, url_prefix="/data")


@data.route("/", methods=["GET", "POST"])
def data_get_add():
    pass
