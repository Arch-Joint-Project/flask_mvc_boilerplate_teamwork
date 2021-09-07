import json

from tests import BaseTestCase
from app.models import AdminModel, LawyerModel
import unittest
import pytest
from datetime import date, time, datetime
from json import JSONEncoder

base_test = BaseTestCase()


class DateTimeEncoder(JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (date, datetime, time)):
            return obj.isoformat()


class TestAdminViews(BaseTestCase):
    @pytest.mark.admin
    def test_admin_view(self):
        response = self.client.get("http://localhost:5000/admin/")
        assert response.status_code == 200
        assert "authentication required" in response.json[0].values()
        headers = base_test.auth("test_admin_username", "test_admin_password")
        response = self.client.get("http://localhost:5000/admin/",
                                   headers=headers)
        assert len(response.json) == 1
        assert "test_admin" in response.json[0].values()

    @pytest.mark.admin
    def test_admin_post(self):
        data = {
            "name": "test_admin",
            "username": "new_username",
            "email": "new_email",
            "password": "test_admin_password"
        }
        response = self.client.post("http://localhost:5000/admin/", json=data)
        assert response.status_code == 201
        assert AdminModel.query.count() == 2
        assert "new_username" in response.json.values()

    @pytest.mark.admin
    def test_admin_lawyer_post(self):
        data = {
            "name": "new_lawyer",
            "username": "new_username",
            "email": "new_email",
            "password": "test_admin_password"
        }
        response = self.client.post("http://localhost:5000/admin/lawyer",
                                    json=data)
        assert response.status_code == 200
        assert "authentication required" in response.json[0].values()
        headers = base_test.auth("test_admin_username", "test_admin_password")
        response = self.client.post("http://localhost:5000/admin/lawyer",
                                    headers=headers, json=data)
        assert response.status_code == 201
        assert LawyerModel.query.count() == 2
        assert "new_username" in response.json.values()

    @pytest.mark.admin
    def test_admin_lawyer_view(self):
        response = self.client.get("http://localhost:5000/admin/lawyer")
        assert response.status_code == 200
        assert "authentication required" in response.json[0].values()
        headers = base_test.auth("test_admin_username", "test_admin_password")
        response = self.client.get("http://localhost:5000/admin/lawyer",
                                   headers=headers)
        assert len(response.json) == 1
        assert "test_lawyer" in response.json[0].values()

    @pytest.mark.admin
    def test_admin_bill_view(self):
        response = self.client.get("http://localhost:5000/admin/bill")
        assert "authentication required" in response.json[0].values()
        headers = base_test.auth("test_admin_username", "test_admin_password")
        response = self.client.get("http://localhost:5000/admin/bill",
                                   headers=headers)
        assert len(response.json) == 1
        assert response.json[0]["lawyer_id"] == 1


class TestLawyerViews(BaseTestCase):
    @pytest.mark.lawyer
    def test_lawyer_view(self):
        response = self.client.get("http://localhost:5000/lawyer/home")
        assert response.status_code == 200
        assert "authentication required" in response.json[0].values()
        headers = base_test.auth("test_lawyer_username", "test_lawyer_password")
        response = self.client.get("http://localhost:5000/lawyer/home",
                                   headers=headers)
        assert "test_lawyer" in response.json.values()
        assert response.json["id"] == 1

    @pytest.mark.lawyer
    def test_lawyer_bill_view(self):
        response = self.client.get("http://localhost:5000/lawyer/bill")
        assert response.status_code == 200
        assert "authentication required" in response.json[0].values()
        headers = base_test.auth("test_lawyer_username", "test_lawyer_password")
        response = self.client.get("http://localhost:5000/lawyer/bill",
                                   headers=headers)
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]["lawyer_id"] == 1

    @pytest.mark.lawyer
    def test_lawyer_company_bill_view(self):
        response = self.client.get(
            "http://localhost:5000/lawyer/bill/company/test_bill_company")
        assert response.status_code == 200
        assert "authentication required" in response.json[0].values()
        headers = base_test.auth("test_lawyer_username", "test_lawyer_password")
        response = self.client.get("http://localhost:5000/lawyer/bill",
                                   headers=headers)
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]["lawyer_id"] == 1

    @pytest.mark.lawyer
    def test_lawyer_delete_bill_view(self):
        response = self.client.delete(
            "http://localhost:5000/lawyer/bill/test_bill_company")
        assert response.status_code == 200
        assert "authentication required" in response.json[0].values()
        headers = base_test.auth("test_lawyer_username", "test_lawyer_password")
        response = self.client.delete("http://localhost:5000/lawyer/bill/test_bill_company",
                                      headers=headers)
        assert response.status_code == 204


if __name__ == "__main__":
    unittest.main()