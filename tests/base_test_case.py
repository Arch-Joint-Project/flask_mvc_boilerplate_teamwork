from flask_testing import TestCase
from app import create_app, db
import fakeredis
from unittest.mock import patch
import pytest
from .initial_test_data import setup_data, model_data
from .test_responses import SharedResponse


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app("config.TestingConfig")
        return app

    def setUp(self):
        """
        Will be called before every test
        """
        db.create_all()
        self.admin, self.lawyer, self.bill = setup_data()
        self.admin_model, self.lawyer_model, self.bill_model = model_data()
        db.session.add(self.admin_model)
        db.session.add(self.lawyer_model)
        db.session.add(self.bill_model)
        db.session.commit()
        self.patcher = patch("app.services.redis_service.redis_conn",
                             fakeredis.FakeStrictRedis())
        self.addCleanup(self.patcher.stop)
        self.redis = self.patcher.start()
        self.shared_responses = SharedResponse()

    def tearDown(self):
        """
        Will be called after every test
        """
        db.session.remove()
        db.drop_all()
        self.patcher.stop()
