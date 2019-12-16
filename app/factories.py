import factory

from app.extensions import db
from app.models import DataModel


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = db.session


class DataFactory(BaseFactory):
    class Meta:
        model = DataModel

    user_id = 1
    value = factory.Faker("pyint")
    unit = factory.Faker("currency_code")
