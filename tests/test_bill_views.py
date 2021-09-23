import unittest
from tests import BaseTestCase
from app.models import BillModel
from app import db
import pytest
from flask import url_for
from datetime import date, time

NO_AUTH_RESPONSE = "Token is missing !!"


class TestBillViews(BaseTestCase):
    @pytest.mark.bill
    def test_signin_admin(self):
        admin_info = {
            "username": "test_admin_username",
            "password": "test_admin_password"
        }
        response = self.client.post(
            url_for("admin.signin_admin"),
            json=admin_info
        )
        return response

    @pytest.mark.bill
    def test_signin_lawyer(self):
        lawyer_info = {
            "username": "test_lawyer_username",
            "password": "test_lawyer_password"
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
        # test without authentication
        response = self.client.post(url_for("bill.create_bill"), json=data)
        assert response.status_code == 401
        assert NO_AUTH_RESPONSE in response.json.values()
        # test with wrong authentication
        sign_in = self.test_signin_admin()
        response = self.client.post(
            url_for("bill.create_bill"),
            headers={"Authorization": "Bearer " + sign_in.json["token"]}, json=data)
        assert response.status_code == 401
        assert "operation unauthorized" in response.json.values()
        # test with valid authentication
        sign_in = self.test_signin_lawyer()
        response = self.client.post(
            url_for("bill.create_bill"),
            headers={"Authorization": "Bearer " + sign_in.json["token"]},
            json=data)
        assert response.status_code == 201
        assert BillModel.query.count() == 2
        assert "test_company" in response.json.values()

    @pytest.mark.bill
    def test_view_bills(self):
        # test without authentication
        response = self.client.get(url_for("bill.view_bills"))
        print(response.json)
        assert response.status_code == 401
        assert NO_AUTH_RESPONSE in response.json.values()
        # test with wrong authentication
        sign_in = self.test_signin_lawyer()
        response = self.client.get(
            url_for("bill.view_bills"),
            headers={"Authorization": "Bearer " + sign_in.json["token"]})
        assert response.status_code == 401
        assert "operation unauthorized" in response.json.values()
        # # test with valid authentication
        sign_in = self.test_signin_admin()
        response = self.client.get(
            url_for("bill.view_bills"),
            headers={"Authorization": "Bearer " + sign_in.json["token"]})
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) == 1

    @pytest.mark.bill
    def test_view_bill(self):
        # test without authentication
        response = self.client.get(url_for("bill.view_bill", bill_id=1))
        assert response.status_code == 401
        assert NO_AUTH_RESPONSE in response.json.values()
        # test with invalid authentication
        sign_in = self.test_signin_lawyer()
        response = self.client.get(
            url_for("bill.view_bill", bill_id=1),
            headers={"Authorization": "Bearer " + sign_in.json["token"]})
        assert response.status_code == 401
        assert "operation unauthorized" in response.json.values()
        # test with valid authentication
        sign_in = self.test_signin_admin()
        response = self.client.get(
            url_for("bill.view_bill", bill_id=1),
            headers={"Authorization": "Bearer " + sign_in.json["token"]})
        assert response.status_code == 200
        assert isinstance(response.json, dict)
        assert "test_bill_company" in response.json.values()

    @pytest.mark.bill
    def test_view_company_bills(self):
        # test without authentication
        response = self.client.get(url_for("bill.view_company_bills", company="test_bill_company"))
        assert response.status_code == 401
        assert NO_AUTH_RESPONSE in response.json.values()
        # test with invalid authentication
        sign_in = self.test_signin_lawyer()
        response = self.client.get(
            url_for("bill.view_company_bills", company="test_bill_company"),
            headers={"Authorization": "Bearer " + sign_in.json["token"]})
        assert response.status_code == 401
        assert "operation unauthorized" in response.json.values()
        # test with valid authentication but wrong query
        sign_in = self.test_signin_admin()
        response = self.client.get(
            url_for("bill.view_company_bills", company="wrong_company"),
            headers={"Authorization": "Bearer " + sign_in.json["token"]})
        assert response.status_code == 200
        assert len(response.json) == 0
        # test with valid authentication and valid query
        sign_in = self.test_signin_admin()
        response = self.client.get(
            url_for("bill.view_company_bills", company="test_bill_company"),
            headers={"Authorization": "Bearer " + sign_in.json["token"]})
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) == 1
        assert "test_bill_company" in response.json[0].values()

    @pytest.mark.bill
    def test_view_lawyer_bills(self):
        # test without authentication
        response = self.client.get(
            url_for("bill.view_lawyer_bills", lawyer_id=1))
        assert response.status_code == 401
        assert NO_AUTH_RESPONSE in response.json.values()
        # test with invalid authentication
        sign_in = self.test_signin_lawyer()
        response = self.client.get(
            url_for("bill.view_lawyer_bills", lawyer_id=1),
            headers={"Authorization": "Bearer " + sign_in.json["token"]})
        assert response.status_code == 401
        assert "operation unauthorized" in response.json.values()
        # test with valid authentication but wrong query
        sign_in = self.test_signin_admin()
        response = self.client.get(
            url_for("bill.view_lawyer_bills", lawyer_id=4),
            headers={"Authorization": "Bearer " + sign_in.json["token"]})
        assert response.status_code == 200
        assert len(response.json) == 0
        # test with valid authentication and valid query
        sign_in = self.test_signin_admin()
        response = self.client.get(
            url_for("bill.view_lawyer_bills", lawyer_id=1),
            headers={"Authorization": "Bearer " + sign_in.json["token"]})
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) == 1
        assert response.json[0].get("lawyer_id") == 1

    @pytest.mark.bill
    def test_update_bill(self):
        data = {
            "billable_rate": 5000,
            "date": "2020-09-09",
            "start_time": "08:30",
            "end_time": "08:30"
        }
        # test without authentication
        response = self.client.put(url_for("bill.update_bill", bill_id=1),
                                   json=data)
        assert response.status_code == 401
        assert NO_AUTH_RESPONSE in response.json.values()
        # test with invalid authentication
        sign_in = self.test_signin_admin()
        response = self.client.put(
            url_for("bill.update_bill", bill_id=1),
            headers={"Authorization": "Bearer " + sign_in.json["token"]},
            json=data,
        )
        assert response.status_code == 401
        assert "operation unauthorized" in response.json.values()
        # test with valid authentication
        sign_in = self.test_signin_lawyer()
        response = self.client.put(
            url_for("bill.update_bill", bill_id=1),
            headers={"Authorization": "Bearer " + sign_in.json["token"]},
            json=data,
        )
        assert response.status_code == 200
        assert BillModel.query.count() == 1
        updated_data = BillModel.query.get(1)
        assert updated_data.billable_rate == response.json.get("billable_rate")

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
        # test without authentication
        assert BillModel.query.count() == 2
        response = self.client.delete(
            url_for("bill.delete_bill", bill_id=2))
        assert response.status_code == 401
        assert NO_AUTH_RESPONSE in response.json.values()
        # test with invalid authentication
        sign_in = self.test_signin_admin()
        response = self.client.delete(
            url_for("bill.delete_bill", bill_id=2),
            headers={"Authorization": "Bearer " + sign_in.json["token"]})
        assert response.status_code == 401
        assert "operation unauthorized" in response.json.values()
        # test with valid authentication
        sign_in = self.test_signin_lawyer()
        response = self.client.delete(
            url_for("bill.delete_bill", bill_id=2),
            headers={"Authorization": "Bearer " + sign_in.json["token"]})
        assert response.status_code == 204
        assert BillModel.query.count() == 1


if __name__ == "__main__":
    unittest.main()
