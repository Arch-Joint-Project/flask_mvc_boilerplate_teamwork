from tests import BaseTestCase
from app.models import AdminModel, LawyerModel, BillModel
import unittest
import pytest


class TestModels(BaseTestCase):
    @pytest.mark.model
    def test_admin_model(self):
        self.assertEqual(AdminModel.query.count(), 1)
        self.assertTrue(AdminModel.query.get(1))
        self.assertEqual(self.admin_model, AdminModel.query.get(1))
        for key in self.admin.keys():
            self.assertEqual(getattr(self.admin_model, key), getattr(AdminModel.query.get(1), key))

    @pytest.mark.model
    def test_lawyer_model(self):
        self.assertEqual(LawyerModel.query.count(), 1)
        self.assertTrue(LawyerModel.query.get(1))
        for key in self.lawyer.keys():
            self.assertEqual(getattr(self.lawyer_model, key), getattr(LawyerModel.query.get(1), key))

    @pytest.mark.model
    def test_bill_model(self):
        self.assertEqual(BillModel.query.count(), 1)
        self.assertTrue(BillModel.query.get(1))
        for key in self.bill.keys():
            self.assertEqual(getattr(self.bill_model, key), getattr(BillModel.query.get(1), key))


if __name__ == "__main__":
    unittest.main()
