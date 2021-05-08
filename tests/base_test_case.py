import os
from flask_testing import TestCase

from app import create_app, db
from config import basedir


class BaseTestCase(TestCase):
    def create_app(self):

        app = create_app()
        app.config.from_object("config.TestingConfig")
        app.config.update(
            SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(basedir, "test.sqlite")
        )

        return app

    def setUp(self):
        """
        Will be called before every test
        """

        db.create_all()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()
