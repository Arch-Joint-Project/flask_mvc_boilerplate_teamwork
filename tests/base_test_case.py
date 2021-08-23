import unittest
from flask_testing import TestCase
from app import create_app
from werkzeug.utils import import_string
from app import db
from app.models import UserModel
import pytest


class BaseTestCase(TestCase):
    def create_app(self):
        # cfg = import_string("config.TestingConfig")()
        app = create_app("config.TestingConfig")
        # app = create_app(cfg)
        app.config.update(
            SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://admin:admin@localhost:5432/test_db"
        )
        return app

    def setUp(self):
        """
        Will be called before every test
        """
        print('this is the testing class')
        # create the database
        db.create_all()
        print('this is after create ')

    def tearDown(self):
        """
        Will be called after every test
        """
        db.session.remove()
        db.drop_all()
