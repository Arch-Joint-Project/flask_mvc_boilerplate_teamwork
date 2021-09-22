import unittest
from random import choice
from tests import BaseTestCase
from app.models import AdminModel, LawyerModel, BillModel
from unittest.mock import patch, Mock
from app import db
import pytest
from flask import url_for
from app.services import AuthService
import fakeredis
# from .test_admin_views import TestAdminViews

# test_admin = TestAdminViews()
# print(test_admin.test_signin_admin())

NO_AUTH_RESPONSE = "Token is missing !!"


@pytest.mark.usefixtures("admin_signin")
class TestLawyerViews(BaseTestCase):
    @pytest.mark.lawyer
    def test_signin_admin(self):
        admin_info = {
            "username": "test_admin_username",
            "password": "test_admin_password"
        }
        response = self.client.post(
            url_for("admin.signin_admin"),
            json=admin_info
        )
        assert response.status_code == 200
        assert "token" in response.json.keys()
        assert len(response.json) == 1
        return response

    @pytest.mark.lawyer
    def test_signin_lawyer(self):
        lawyer_info = {
            "username": "test_lawyer_username",
            "password": "test_lawyer_password"
        }
        response = self.client.post(
            url_for("lawyer.signin_lawyer"),
            json=lawyer_info
        )
        assert response.status_code == 200
        assert "token" in response.json.keys()
        assert len(response.json) == 1
        return response

    @pytest.mark.lawyer
    def test_create_lawyer(self):
        data = {
            "name": "create_lawyer",
            "username": "create_username",
            "email": "create_email",
            "password": "create_password"
        }
        # test without authentication
        response = self.client.post(url_for("lawyer.create_lawyer"),
                                    json=data)
        assert response.status_code == 401
        assert NO_AUTH_RESPONSE in response.json.values()
        # test with wrong authentication
        sign_in = self.test_signin_lawyer()
        response = self.client.post(
            url_for("lawyer.create_lawyer"),
            headers={"Authorization": "Bearer " + sign_in.json["token"]}, json=data)
        assert response.status_code == 401
        assert "operation unauthorized" in response.json.values()
        # test with valid authentication
        sign_in = self.test_signin_admin()
        response = self.client.post(
            url_for("lawyer.create_lawyer"),
            headers={"Authorization": "Bearer " + sign_in.json["token"]},
            json=data)
        assert response.status_code == 201
        assert LawyerModel.query.count() == 2
        assert "create_lawyer" in response.json.values()

    @pytest.mark.lawyer
    def test_view_lawyers(self):
        # test without authentication
        response = self.client.get(url_for("lawyer.view_lawyers"))
        assert response.status_code == 401
        assert NO_AUTH_RESPONSE in response.json.values()
        # test with wrong authentication
        sign_in = self.test_signin_lawyer()
        response = self.client.get(
            url_for("lawyer.view_lawyers"),
            headers={"Authorization": "Bearer " + sign_in.json["token"]})
        assert response.status_code == 401
        assert "operation unauthorized" in response.json.values()
        # # test with valid authentication
        sign_in = self.test_signin_admin()
        response = self.client.get(
            url_for("lawyer.view_lawyers"),
            headers={"Authorization": "Bearer " + sign_in.json["token"]})
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) == 1

    @pytest.mark.lawyer
    def test_view_lawyer(self):
        # test without authentication
        response = self.client.get(url_for("lawyer.view_lawyer", lawyer_id=1))
        assert response.status_code == 401
        assert NO_AUTH_RESPONSE in response.json.values()
        # test with invalid authentication
        sign_in = self.test_signin_lawyer()
        response = self.client.get(
            url_for("lawyer.view_lawyer", lawyer_id=1),
            headers={"Authorization": "Bearer " + sign_in.json["token"]})
        assert response.status_code == 401
        assert "operation unauthorized" in response.json.values()
        # test with valid authentication
        sign_in = self.test_signin_admin()
        response = self.client.get(
            url_for("lawyer.view_lawyer", lawyer_id=1),
            headers={"Authorization": "Bearer " + sign_in.json["token"]})
        assert response.status_code == 200
        assert isinstance(response.json, dict)
        assert "test_lawyer" in response.json.values()

    @pytest.mark.lawyer
    def test_update_lawyer(self):
        data = {
            "name": "update_lawyer",
            "username": "update_username",
            "email": "update_email",
            "password": "update_password"
        }
        # test without authentication
        response = self.client.put(url_for("lawyer.update_lawyer", lawyer_id=1),
                                   json=data)
        assert response.status_code == 401
        assert NO_AUTH_RESPONSE in response.json.values()
        # test with invalid authentication
        sign_in = self.test_signin_lawyer()
        response = self.client.put(
            url_for("lawyer.update_lawyer", lawyer_id=1),
            headers={"Authorization": "Bearer " + sign_in.json["token"]},
            json=data,
            )
        assert response.status_code == 401
        assert "operation unauthorized" in response.json.values()
        # test with valid authentication
        sign_in = self.test_signin_admin()
        response = self.client.put(
            url_for("lawyer.update_lawyer", lawyer_id=1),
            headers={"Authorization": "Bearer " + sign_in.json["token"]},
            json=data,
        )
        assert response.status_code == 200
        assert LawyerModel.query.count() == 1
        updated_data = LawyerModel.query.get(1)
        for key in response.json.keys():
            assert response.json[key] == getattr(updated_data, key)

    @pytest.mark.lawyer
    def test_delete_lawyer(self):
        new_lawyer = LawyerModel(
            admin_id=1,
            name="test_delete_lawyer",
            username="test_delete_admin_username",
            email="test_delete_admin_email",
            password="test_delete_admin_password"
        )
        db.session.add(new_lawyer)
        db.session.commit()
        # test without authentication
        assert LawyerModel.query.count() == 2
        response = self.client.delete(
            url_for("lawyer.delete_lawyer", lawyer_id=2))
        assert response.status_code == 401
        assert NO_AUTH_RESPONSE in response.json.values()
        # test with invalid authentication
        sign_in = self.test_signin_lawyer()
        response = self.client.delete(
            url_for("lawyer.delete_lawyer", lawyer_id=2),
            headers={"Authorization": "Bearer " + sign_in.json["token"]})
        assert response.status_code == 401
        assert "operation unauthorized" in response.json.values()
        # test with valid authentication
        sign_in = self.test_signin_admin()
        response = self.client.delete(
            url_for("lawyer.delete_lawyer", lawyer_id=2),
            headers={"Authorization": "Bearer " + sign_in.json["token"]})
        assert response.status_code == 204
        assert AdminModel.query.count() == 1


if __name__ == "__main__":
    unittest.main()
