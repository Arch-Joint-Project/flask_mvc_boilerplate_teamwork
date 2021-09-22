from tests import BaseTestCase
from app.models import AdminModel, LawyerModel, BillModel
import unittest
from datetime import date, time


class TestModels(BaseTestCase):
    def test_admin_model(self):
        assert AdminModel.query.count() == 1
        admin_data = AdminModel.query.all()
        assert admin_data[0].name == "test_admin"
        assert admin_data[0].username == "test_admin_username"
        assert admin_data[0].email == "test_admin_email"
        assert admin_data[0].verify_password("test_admin_password")

    def test_lawyer_model(self):
        assert LawyerModel.query.count() == 1
        lawyer_data = LawyerModel.query.all()
        assert lawyer_data[0].name == "test_lawyer"
        assert lawyer_data[0].username == "test_lawyer_username"
        assert lawyer_data[0].email == "test_lawyer_email"
        assert lawyer_data[0].verify_password("test_lawyer_password")

    def test_bill_model(self):
        assert BillModel.query.count() == 1
        bill_data = BillModel.query.all()
        assert bill_data[0].lawyer_id == 1
        assert bill_data[0].billable_rate == 300
        assert bill_data[0].company == "test_bill_company"
        assert bill_data[0].date == date(2020, 1, 4)
        assert bill_data[0].start_time == time(8, 0)
        assert bill_data[0].end_time == time(20, 0)


if __name__ == "__main__":
    unittest.main()
