from .base_test_case import BaseTestCase
from app.models import AdminModel, LawyerModel, BillModel
import unittest
from app import db


class TestModels(BaseTestCase):
    def test_admin_model(self):
        assert AdminModel.query.count() == 1
        admin_data = AdminModel.query.all()
        print(admin_data[0])
        assert admin_data[0].name == "test_admin"
        assert admin_data[0].username == "test_admin_username"
        assert admin_data[0].email == "test_admin_email"
        assert admin_data[0].password == "test_admin_password"

    def test_lawyer_model(self):
        assert LawyerModel.query.count() == 1

    def test_bill_model(self):
        assert BillModel.query.count() == 1




if __name__ == "__main__":
    unittest.main()
