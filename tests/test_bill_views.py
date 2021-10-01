import unittest
from tests import BaseTestCase, SharedResponse
from app.models import BillModel
from app import db
import pytest
from flask import url_for
from datetime import date, time

shared_response = SharedResponse()


class TestBillViews(BaseTestCase):
    @pytest.mark.bill
    def test_signin_admin(self):
        admin_info = {
            "username": self.admin_data["username"],
            "password": self.admin_data["password"]
        }
        response = self.client.post(
            url_for("admin.signin_admin"),
            json=admin_info
        )
        return response

    @pytest.mark.bill
    def test_signin_lawyer(self):
        lawyer_info = {
            "username": self.lawyer_data["username"],
            "password": self.lawyer_data["password"]
        }
        response = self.client.post(
            url_for("lawyer.signin_lawyer"),
            json=lawyer_info
        )
        return response

    @pytest.mark.bill
    def test_create_bill(self):
        data = {
            "billable_rate": 300,
            "company": "test_company",
            "date": "2020-09-09",
            "start_time": "08:30",
            "end_time": "08:30"
        }
        # no token
        response = self.client.post(url_for("bill.create_bill"), json=data)
        assert response.status_code == 401
        assert shared_response.missing_token_authentication() == response.json
        # wrong access token
        sign_in = self.test_signin_admin()
        response = self.client.post(
            url_for("bill.create_bill"),
            headers={"Authorization": "Bearer " + sign_in.json["access_token"]}, json=data)
        assert response.status_code == 401
        assert shared_response.unauthorize_operation() == response.json
        # access token
        sign_in = self.test_signin_lawyer()
        response = self.client.post(
            url_for("bill.create_bill"),
            headers={"Authorization": "Bearer " + sign_in.json["access_token"]},
            json=data)
        assert response.status_code == 201
        assert isinstance(response.json, dict)
        assert BillModel.query.count() == 2
        assert "test_company" in response.json.values()
        assert "test_company" == BillModel.query.get(2).company

    @pytest.mark.bill
    def test_view_bills(self):
        sign_in = self.test_signin_admin()
        response = self.client.get(
            url_for("bill.view_bills"),
            headers={"Authorization": "Bearer " + sign_in.json["access_token"]})
        assert response.status_code == 200
        assert isinstance(response.json, list)

    @pytest.mark.bill
    def test_view_bill(self):
        sign_in = self.test_signin_admin()
        # unavailable resource
        response = self.client.get(url_for("bill.view_bill", bill_id=2),
                                   headers={"Authorization": "Bearer " +
                                            sign_in.json["access_token"]})
        assert response.status_code == 404
        assert isinstance(response.json, dict)
        assert shared_response.resource_unavailable() == response.json
        # available resource
        response = self.client.get(
            url_for("bill.view_bill", bill_id=1),
            headers={"Authorization": "Bearer " + sign_in.json["access_token"]})
        assert response.status_code == 200
        assert isinstance(response.json, dict)
        assert self.bill_data["company"] in response.json.values()

    @pytest.mark.active
    def test_view_company_bills(self):
        sign_in = self.test_signin_admin()
        # unavailable resource
        response = self.client.get(
            url_for("bill.view_company_bills", company="wrong_company"),
            headers={"Authorization": "Bearer " + sign_in.json["access_token"]})
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert response.json == []
        # available resource
        response = self.client.get(
            url_for("bill.view_company_bills", company=self.bill_data["company"]),
            headers={"Authorization": "Bearer " + sign_in.json["access_token"]})
        assert response.status_code == 200
        assert isinstance(response.json, list)
        print(response.json)
        assert self.bill_data["company"] in response.json[0].values()

    @pytest.mark.bill
    def test_view_lawyer_bills(self):
        sign_in = self.test_signin_admin()
        response = self.client.get(
            url_for("bill.view_lawyer_bills", lawyer_id=1),
            headers={"Authorization": "Bearer " + sign_in.json["access_token"]})
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert response.json[0].get("company") == self.bill_data["company"]

    @pytest.mark.bill
    def test_update_bill(self):
        data = {
            "billable_rate": 5000,
            "company": "updated_company",
            "date": "2020-09-09",
            "start_time": "08:30",
            "end_time": "08:30"
        }
        sign_in = self.test_signin_lawyer()
        response = self.client.put(
            url_for("bill.update_bill", bill_id=1),
            headers={"Authorization": "Bearer " + sign_in.json["access_token"]},
            json=data,
        )
        assert response.status_code == 200
        assert BillModel.query.count() == 1
        assert "updated_company" == BillModel.query.get(1).company

    @pytest.mark.bill
    def test_delete_bill(self):
        new_bill = BillModel(
            lawyer_id=1,
            billable_rate=500,
            company="test_delete_company",
            date=date(2020, 1, 4),
            start_time=time(8, 0),
            end_time=time(20, 0)
        )
        db.session.add(new_bill)
        db.session.commit()
        assert BillModel.query.count() == 2
        sign_in = self.test_signin_lawyer()
        response = self.client.delete(
            url_for("bill.delete_bill", bill_id=2),
            headers={"Authorization": "Bearer " + sign_in.json["access_token"]})
        assert response.status_code == 204
        assert BillModel.query.count() == 1


if __name__ == "__main__":
    unittest.main()
