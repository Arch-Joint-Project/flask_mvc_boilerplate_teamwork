# import os
# import tempfile
# import flask
#
# import pytest
#
# from app import create_app, db
#
# flask_app = flask.Flask(__name__)
#
#
# @pytest.fixture
# def client():
#     app = create_app()
#     app.config.from_object("config.DevelopmentConfig")
#     with app.app_context():
#         db.create_all()
#         yield app  # Note that we changed return for yield, see below for why
#         db.drop_all()
#
#
# def create_user(client, name, email):
#     return client.post("/api/users", data=dict(name=name, email=email))
#
#
# def test_create_user(client):
#     user = create_user(client, "John Doe", "john@example.com")
#     assert user.name == "John Doe"

import unittest
import os
from flask import abort, url_for
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
