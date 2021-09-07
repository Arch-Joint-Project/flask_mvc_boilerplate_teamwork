from flask_testing import TestCase
from app import create_app, db
from app.models import AdminModel, LawyerModel, BillModel
from datetime import datetime, date, time
from werkzeug.security import generate_password_hash


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app("config.TestingConfig")
        return app

    def setUp(self):
        """
        Will be called before every test
        """
        db.create_all()
        admin = AdminModel(
            name="test_admin",
            username="test_admin_username",
            email="test_admin_email",
            password=generate_password_hash("test_admin_password", method="sha256")
        )
        lawyer = LawyerModel(
            admin_id=1,
            name="test_lawyer",
            username="test_lawyer_username",
            email="test_lawyer_email",
            password=generate_password_hash("test_lawyer_password", method="sha256")
        )
        bill = BillModel(
            lawyer_id=1,
            billable_rate=300,
            company="test_bill_company",
            date=date(2020, 1, 4),
            start_time=time(8, 0),
            end_time=time(20, 0)
        )
        db.session.add(admin)
        db.session.add(lawyer)
        db.session.add(bill)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """
        db.session.remove()
        db.drop_all()
