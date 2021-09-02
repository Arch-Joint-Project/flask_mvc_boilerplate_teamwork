from .base_test_case import BaseTestCase
from app.models import AdminModel, LawyerModel, BillModel
import unittest
from app import db


class TestViews(BaseTestCase):
    def test_admin_view(self):
        response = self.client.get("http://localhost:5000/admin/")
        print(response.json)
        print(len(response.json[0].values()))
        assert response.status_code == 200
        assert len(response.json) == 1
        assert "test_admin" in response.json[0].values()

    def test_admin_post(self):
        data = {
            "name": "test_admin",
            "username": "new_username",
            "email": "new_email",
            "password": "test_admin_password"
        }
        response = self.client.post("http://localhost:5000/admin/", json=data)
        print(f'this {response.json}')
        assert response.status_code == 201
        assert AdminModel.query.count() == 2
        assert "new_username" in response.json.values()

    def test_lawyer_view(self):
        response = self.client.get("http://localhost:5000/lawyer/")
        print(response.json)
        print(len(response.json[0].values()))
        assert response.status_code == 200
        assert len(response.json) == 1
        assert "test_lawyer" in response.json[0].values()

    def test_lawyer_post(self):
        data = {
            "admin_id": 1,
            "name": "new_lawyer",
            "username": "new_username",
            "email": "new_email",
            "password": "test_admin_password"
        }
        response = self.client.post("http://localhost:5000/lawyer/", json=data)
        print(f'this {response.json}')
        assert response.status_code == 201
        assert LawyerModel.query.count() == 2
        assert "new_username" in response.json.values()

    def test_bill_view(self):
        response = self.client.get("http://localhost:5000/bill/")
        print(response.json)
        print(len(response.json[0].values()))
        assert response.status_code == 200
        assert len(response.json) == 1
        assert "test_bill_company" in response.json[0].values()

    def test_bill_post(self):
        data = {
            "admin_id": 1,
            "name": "new_lawyer",
            "username": "new_username",
            "email": "new_email",
            "password": "test_admin_password"
        }
        response = self.client.post("http://localhost:5000/lawyer/", json=data)
        print(f'this {response.json}')
        assert response.status_code == 201
        assert LawyerModel.query.count() == 2
        assert "new_username" in response.json.values()


if __name__ == "__main__":
    unittest.main()
