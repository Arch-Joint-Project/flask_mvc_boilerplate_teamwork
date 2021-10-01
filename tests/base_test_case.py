import json
from flask_testing import TestCase
from app import create_app, db
from app.models import AdminModel, LawyerModel, BillModel
from datetime import date, time
import fakeredis
from unittest.mock import patch
import pytest
from .test_responses import SharedResponse

shared_data = SharedResponse()


@pytest.mark.usefixtures("initial_data")
class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app("config.TestingConfig")
        return app

    def setUp(self):
        """
        Will be called before every test
        """
        db.create_all()
        print("this is self", self.admin_data)
        admin = AdminModel(**self.admin_data)
        lawyer = LawyerModel(**self.lawyer_data)
        bill = BillModel(**self.bill_data)
        # admin = AdminModel(
        #     name=initial_admin_info["name"],
        #     username=initial_admin_info["username"],
        #     email=initial_admin_info["email"],
        #     password=initial_admin_info["password"]
        # )
        # lawyer = LawyerModel(
        #     admin_id=1,
        #     name="test_lawyer",
        #     username="test_lawyer_username",
        #     email="test_lawyer_email",
        #     password="test_lawyer_password"
        # )
        # bill = BillModel(
        #     lawyer_id=1,
        #     billable_rate=300,
        #     company="test_bill_company",
        #     date=date(2020, 1, 4),
        #     start_time=time(8, 0),
        #     end_time=time(20, 0)
        # )
        db.session.add(admin)
        db.session.add(lawyer)
        db.session.add(bill)
        db.session.commit()
        self.patcher = patch("app.services.redis_service.redis_conn",
                             fakeredis.FakeStrictRedis())
        self.addCleanup(self.patcher.stop)
        self.redis = self.patcher.start()
        # self.redis.set(f"admin__{self.admin_info.get('id')}",
        #                json.dumps(self.admin_info))
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
