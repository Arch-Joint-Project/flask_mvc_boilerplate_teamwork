from app.controllers import BillController
from app.repositories import BillRepository
from tests import BaseTestCase
import pytest
from app.models import BillModel
import unittest
from app.core.service_result import ServiceResult


NEW_BILL = {
    "lawyer_id": 1,
    "billable_rate": 300,
    "company": "new_company",
    "date": "2020-09-09",
    "start_time": "08:30",
    "end_time": "08:30"
}
UPDATE_BILL_INFO = {
    "lawyer_id": 1,
    "billable_rate": 5000,
    "company": "update_company",
    "date": "2020-12-12",
    "start_time": "06:30",
    "end_time": "20:30"
}


class TestBillController(BaseTestCase):
    @pytest.mark.bill
    def test_index(self):
        get_all_bills = BillController(BillRepository(self.redis)).index()
        self.assertEqual(BillModel.query.count(), 1)
        self.assertIsInstance(get_all_bills, ServiceResult)
        self.assertTrue(get_all_bills.success)
        self.assert200(get_all_bills.data)
        self.assertEqual(get_all_bills.exception_case, None)

    @pytest.mark.bill
    def test_create(self):
        new_bill = NEW_BILL.copy()
        create_new_bill = BillController(BillRepository(self.redis)).create(1, new_bill)
        self.assertEqual(BillModel.query.count(), 2)
        self.assertIsInstance(create_new_bill, ServiceResult)
        self.assertTrue(create_new_bill.success)
        self.assertEqual(create_new_bill.data.status_code, 201)
        self.assertEqual(create_new_bill.exception_case, None)

    @pytest.mark.bill
    def test_find_by_id(self):
        find_bill_by_id = BillController(BillRepository(self.redis)).find_by_id(1)
        self.assertEqual(BillModel.query.count(), 1)
        self.assertIsInstance(find_bill_by_id, ServiceResult)
        self.assertTrue(find_bill_by_id.success)
        self.assert200(find_bill_by_id.data)
        self.assertEqual(find_bill_by_id.exception_case, None)

    @pytest.mark.bill
    def test_find_all(self):
        find_all_bill = BillController(
            BillRepository(self.redis)).find_all({"company": self.bill["company"]})
        self.assertEqual(BillModel.query.count(), 1)
        self.assertIsInstance(find_all_bill, ServiceResult)
        self.assertTrue(find_all_bill.success)
        self.assert200(find_all_bill.data)
        self.assertEqual(find_all_bill.exception_case, None)

    @pytest.mark.bill
    def test_update_by_id(self):
        update_bill = BillController(BillRepository(self.redis)).update_by_id(1, UPDATE_BILL_INFO, 1)
        self.assertEqual(BillModel.query.count(), 1)
        self.assertIsInstance(update_bill, ServiceResult)
        self.assertTrue(update_bill.success)
        self.assert200(update_bill.data)
        self.assertEqual(update_bill.exception_case, None)

    @pytest.mark.bill
    def test_delete(self):
        new_bill = NEW_BILL.copy()
        BillController(BillRepository(self.redis)).create(1, new_bill)
        self.assertEqual(BillModel.query.count(), 2)
        delete_bill = BillController(BillRepository(self.redis)).delete(2, 1)
        self.assertEqual(BillModel.query.count(), 1)
        self.assertIsInstance(delete_bill, ServiceResult)
        self.assertTrue(delete_bill.success)
        self.assertEqual(delete_bill.data.status_code, 204)
        self.assertEqual(delete_bill.exception_case, None)


if __name__ == "__main__":
    unittest.main()
