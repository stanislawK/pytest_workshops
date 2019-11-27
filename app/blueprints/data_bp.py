from flask import Blueprint, render_template

data = Blueprint("data", __name__, url_prefix="/data")


@data.route("/", methods=["GET"])
def index():
    user = "unknown"
    return render_template("index.html", user=user)
