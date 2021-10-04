import unittest
from tests import BaseTestCase, SharedResponse
from app.models import BillModel
from app import db
import pytest
from flask import url_for
from datetime import date, time

NEW_BILL = {
    "billable_rate": 300,
    "company": "new_company",
    "date": "2020-09-09",
    "start_time": "08:30",
    "end_time": "08:30"
}
UPDATE_BILL_INFO = {
    "billable_rate": 5000,
    "company": "update_company",
    "date": "2020-12-12",
    "start_time": "06:30",
    "end_time": "20:30"
}


class TestBillViews(BaseTestCase):
    @pytest.mark.bill
    def test_signin_admin(self):
        admin_info = {
            "username": self.admin["username"],
            "password": self.admin["password"]
        }
        response = self.client.post(
            url_for("admin.signin_admin"),
            json=admin_info
        )
        return response

    @pytest.mark.bill
    def test_signin_lawyer(self):
        lawyer_info = {
            "username": self.lawyer["username"],
            "password": self.lawyer["password"]
        }
        response = self.client.post(
            url_for("lawyer.signin_lawyer"),
            json=lawyer_info
        )
        return response

    @pytest.mark.bill
    def test_create_bill(self):
        admin_sign_in = self.test_signin_admin()
        lawyer_sign_in = self.test_signin_lawyer()
        new_bill = NEW_BILL.copy()
        no_token_response = self.client.get(url_for("bill.create_bill"), json=new_bill)
        self.assert401(no_token_response)
        self.assertIsInstance(no_token_response.json, dict)
        self.assertEqual(no_token_response.json,
                         self.shared_responses.missing_token_authentication())
        wrong_access_token_response = self.client.post(
            url_for("bill.create_bill"),
            headers={"Authorization": "Bearer " +
                                      admin_sign_in.json["access_token"]
                     }, json=new_bill
        )
        self.assert401(wrong_access_token_response)
        self.assertIsInstance(wrong_access_token_response.json, dict)
        self.assertEqual(wrong_access_token_response.json,
                         self.shared_responses.unauthorize_operation())
        right_access_token_response = self.client.post(
            url_for("bill.create_bill"),
            headers={"Authorization": "Bearer "
                                      + lawyer_sign_in.json["access_token"]
                     }, json=new_bill
        )
        self.assertEqual(right_access_token_response.status_code, 201)
        self.assertEqual(BillModel.query.count(), 2)
        self.assertIsInstance(right_access_token_response.json, dict)
        self.assertTrue(BillModel.query.get(2))
        self.assertEqual(right_access_token_response.json["company"],
                         new_bill["company"])

    @pytest.mark.bill
    def test_view_bills(self):
        sign_in = self.test_signin_admin()
        response = self.client.get(
            url_for("bill.view_bills"),
            headers={
                "Authorization": "Bearer " + sign_in.json["access_token"]})
        self.assertEqual(BillModel.query.count(), 1)
        self.assert200(response)
        self.assertIsInstance(response.json, list)
        self.assertIsInstance(response.json[0], dict)
        for key in response.json[0].keys():
            self.assertEqual(getattr(self.bill_model, key),
                             getattr(BillModel.query.get(1), key))

    @pytest.mark.bill
    def test_view_bill(self):
        sign_in = self.test_signin_admin()
        resource_unavailable_response = self.client.get(
            url_for("bill.view_bill", bill_id=2),
            headers={"Authorization": "Bearer " + sign_in.json["access_token"]}
        )
        self.assert404(resource_unavailable_response)
        self.assertIsInstance(resource_unavailable_response.json, dict)
        self.assertEqual(resource_unavailable_response.json,
                         self.shared_responses.resource_unavailable())
        resource_available_response = self.client.get(
            url_for("bill.view_bill", bill_id=1),
            headers={"Authorization": "Bearer " + sign_in.json["access_token"]}
        )
        self.assertEqual(BillModel.query.count(), 1)
        self.assert200(resource_available_response)
        self.assertIsInstance(resource_available_response.json, dict)
        self.assertEqual(resource_available_response.json["company"], self.bill["company"])

    @pytest.mark.bill
    def test_view_company_bills(self):
        sign_in = self.test_signin_admin()
        resource_unavailable_response = self.client.get(
            url_for("bill.view_company_bills", company="wrong_company"),
            headers={"Authorization": "Bearer " + sign_in.json["access_token"]}
        )
        self.assert200(resource_unavailable_response)
        self.assertIsInstance(resource_unavailable_response.json, list)
        resource_available_response = self.client.get(
            url_for("bill.view_company_bills", company=self.bill["company"]),
            headers={"Authorization": "Bearer " + sign_in.json["access_token"]}
        )
        self.assertEqual(BillModel.query.count(), 1)
        self.assert200(resource_available_response)
        self.assertIsInstance(resource_available_response.json, list)
        self.assertIsInstance(resource_available_response.json[0], dict)
        self.assertEqual(resource_available_response.json[0]["company"], self.bill["company"])

    @pytest.mark.bill
    def test_view_lawyer_bills(self):
        sign_in = self.test_signin_admin()
        response = self.client.get(
            url_for("bill.view_lawyer_bills", lawyer_id=1),
            headers={"Authorization": "Bearer " + sign_in.json["access_token"]})
        self.assert200(response)
        self.assertEqual(BillModel.query.count(), 1)
        self.assertIsInstance(response.json, list)
        self.assertIsInstance(response.json[0], dict)
        self.assertEqual(response.json[0]["id"], 1)

    @pytest.mark.bill
    def test_update_bill(self):
        update_bill = UPDATE_BILL_INFO.copy()
        sign_in = self.test_signin_lawyer()
        response = self.client.put(
            url_for("bill.update_bill", bill_id=1),
            headers={"Authorization": "Bearer " + sign_in.json["access_token"]},
            json=update_bill,
        )
        self.assert200(response)
        self.assertEqual(BillModel.query.count(), 1)
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["company"], update_bill["company"])

    @pytest.mark.bill
    def test_delete_bill(self):
        sign_in = self.test_signin_lawyer()
        new_bill = NEW_BILL.copy()
        self.client.post(url_for("bill.create_bill"),
            headers={"Authorization": "Bearer " + sign_in.json["access_token"]}
            , json=new_bill
        )
        self.assertEqual(BillModel.query.count(), 2)
        delete_admin_response = self.client.delete(
            url_for("bill.delete_bill", bill_id=2),
            headers={"Authorization": "Bearer " + sign_in.json["access_token"]}
        )
        self.assertEqual(delete_admin_response.status_code, 204)
        self.assertEqual(BillModel.query.count(), 1)


if __name__ == "__main__":
    unittest.main()
