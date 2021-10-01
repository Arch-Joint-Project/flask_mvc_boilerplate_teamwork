from tests import BaseTestCase
from app.models import AdminModel, LawyerModel, BillModel
import unittest
from datetime import date, time
import pytest


@pytest.mark.usefixtures("initial_data")
class TestModels(BaseTestCase):
    @pytest.mark.model
    def test_admin_model(self):
        assert AdminModel.query.count() == 1
        admin_data = AdminModel.query.all()
        assert admin_data[0].name == self.admin_data["name"]
        assert admin_data[0].username == self.admin_data["username"]
        assert admin_data[0].email == self.admin_data["email"]
        assert admin_data[0].verify_password(self.admin_data["password"])

    @pytest.mark.model
    def test_lawyer_model(self):
        assert LawyerModel.query.count() == 1
        lawyer_data = LawyerModel.query.all()
        assert lawyer_data[0].name == self.lawyer_data["name"]
        assert lawyer_data[0].username == self.lawyer_data["username"]
        assert lawyer_data[0].email == self.lawyer_data["email"]
        assert lawyer_data[0].verify_password(self.lawyer_data["password"])

    @pytest.mark.model
    def test_bill_model(self):
        assert BillModel.query.count() == 1
        bill_data = BillModel.query.all()
        assert bill_data[0].lawyer_id == 1
        assert bill_data[0].billable_rate == self.bill_data["billable_rate"]
        assert bill_data[0].company == self.bill_data["company"]
        assert bill_data[0].date == self.bill_data["date"]
        assert bill_data[0].start_time == self.bill_data["start_time"]
        assert bill_data[0].end_time == self.bill_data["end_time"]


if __name__ == "__main__":
    unittest.main()
