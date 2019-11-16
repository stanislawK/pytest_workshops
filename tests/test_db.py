from app.models import UserModel


def test_save_user_to_db(_db, new_user):
    assert not _db.session.query(UserModel).all()

    user = UserModel(**new_user)
    _db.session.add(user)
    _db.session.commit()

    user_db = _db.session.query(UserModel).first()
    assert user_db == user
