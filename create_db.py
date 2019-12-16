from app.app_factory import create_app
from app.extensions import db

app = create_app()

with app.app_context():
    db.create_all()
