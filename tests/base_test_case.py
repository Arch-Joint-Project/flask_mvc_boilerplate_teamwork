import json

from flask_testing import TestCase
from app import create_app, db
from app.models import AdminModel, LawyerModel, BillModel
from datetime import date, time
import fakeredis
from unittest.mock import patch
import pytest


@pytest.mark.usefixtures("base_test_case_setup_requirement")
class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app("config.TestingConfig")
        return app

    def setUp(self):
        """
        Will be called before every test
        """
        db.create_all()
        admin = AdminModel(**self.init_admin_info)
        lawyer = LawyerModel(**self.init_lawyer_info)
        bill = BillModel(**self.init_bill_info)
        db.session.add(admin)
        db.session.add(lawyer)
        db.session.add(bill)
        db.session.commit()
        self.patcher = patch("app.services.redis_service.redis_conn",
                             fakeredis.FakeStrictRedis())
        self.addCleanup(self.patcher.stop)
        self.redis = self.patcher.start()
        # self.redis.set(f"admin__{self.init_admin_info.get('id')}",
        #                json.dumps(self.init_admin_info))
        # self.redis.set(f"lawyer__{self.init_lawyer_info.get('id')}",
        #                json.dumps(self.init_lawyer_info))
        # self.redis.set(f"bill__{self.init_bill_info.get('id')}",
        #                json.dumps(self.init_bill_info))

    def tearDown(self):
        """
        Will be called after every test
        """
        db.session.remove()
        db.drop_all()
        self.patcher.stop()
