from .base_test_case import BaseTestCase
from app.models import User
from app import db


class UserMigrationTestCase(BaseTestCase):
    def test_create_user(self):
        user = User(name="Maclean", email="maclean@example.com")
        db.session.add(user)
        db.session.commit()

        self.assertEqual(user.name, "Maclean", "Not equal")

    def test_edit_user(self):
        user = User(name="Maclean", email="maclean@example.com")
        db.session.add(user)
        db.session.commit()

        self.assertEqual(user.name, "Maclean", "Not equal")

        user_search = User.query.filter_by(name='Maclean').first()
        self.assertEqual(user_search.name, "Maclean")

