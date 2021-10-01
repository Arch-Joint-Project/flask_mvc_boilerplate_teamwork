import unittest
from tests import BaseTestCase, SharedResponse
from app.models import LawyerModel
from app import db
import pytest
from flask import url_for

shared_response = SharedResponse()


@pytest.mark.usefixtures("initial_data")
class TestLawyerViews(BaseTestCase):
    @pytest.mark.lawyer
    def test_signin_admin(self):
        # valid credentials
        admin_info = {
            "username": self.admin_data["username"],
            "password": self.admin_data["password"]
        }
        response = self.client.post(
            url_for("admin.signin_admin"),
            json=admin_info
        )
        return response

    @pytest.mark.lawyer
    def test_signin_lawyer(self):
        # without invalid credential
        lawyer_info = {
            "username": "tes_lawyer",
            "password": "test_lawyer_password"
        }
        response = self.client.post(
            url_for("lawyer.signin_lawyer"),
            json=lawyer_info
        )
        assert response.status_code == 200
        assert isinstance(response.json, dict)
        assert len(shared_response.signin_invalid_credentials()) == \
               len(response.json)
        assert shared_response.signin_invalid_credentials() == \
               response.json
        # valid credential
        lawyer_info = {
            "username": self.lawyer_data["username"],
            "password": self.lawyer_data["password"]
        }
        response = self.client.post(
            url_for("lawyer.signin_lawyer"),
            json=lawyer_info
        )
        assert response.status_code == 200
        assert isinstance(response.json, dict)
        assert len(shared_response.signin_valid_credentials()) == \
               len(response.json)
        assert shared_response.signin_valid_credentials().keys() == \
               response.json.keys()
        return response

    @pytest.mark.lawyer
    def test_create_lawyer(self):
        data = {
            "name": "create_lawyer",
            "username": "create_username",
            "email": "create_email",
            "password": "create_password"
        }
        # without token
        response = self.client.post(url_for("lawyer.create_lawyer"),
                                    json=data)
        assert response.status_code == 401
        assert shared_response.missing_token_authentication() == response.json
        # wrong access token
        sign_in = self.test_signin_lawyer()
        response = self.client.post(
            url_for("lawyer.create_lawyer"),
            headers={
                "Authorization": "Bearer " + sign_in.json["access_token"]},
            json=data)
        assert response.status_code == 401
        assert shared_response.unauthorize_operation() == response.json
        # test with valid authentication
        sign_in = self.test_signin_admin()
        print(sign_in)
        response = self.client.post(
            url_for("lawyer.create_lawyer"),
            headers={
                "Authorization": "Bearer " + sign_in.json["access_token"]},
            json=data)
        assert response.status_code == 201
        assert LawyerModel.query.count() == 2
        assert isinstance(response.json, dict)
        for key in response.json.keys():
            assert response.json[key] == getattr(LawyerModel.query.get(2), key)

    @pytest.mark.lawyer
    def test_view_lawyers(self):
        sign_in = self.test_signin_admin()
        response = self.client.get(
            url_for("lawyer.view_lawyers"),
            headers={
                "Authorization": "Bearer " + sign_in.json["access_token"]})
        assert response.status_code == 200
        assert isinstance(response.json, list)
        for key in response.json[0].keys():
            assert response.json[0][key] == getattr(LawyerModel.query.get(1), key)

    @pytest.mark.lawyer
    def test_view_lawyer(self):
        # unavailable user
        sign_in = self.test_signin_admin()
        response = self.client.get(
            url_for("lawyer.view_lawyer", lawyer_id=2),
            headers={
                "Authorization": "Bearer " + sign_in.json["access_token"]})
        assert response.status_code == 404
        assert isinstance(response.json, dict)
        assert shared_response.resource_unavailable() == response.json
        #  available user
        response = self.client.get(
            url_for("lawyer.view_lawyer", lawyer_id=1),
            headers={
                "Authorization": "Bearer " + sign_in.json["access_token"]})
        assert response.status_code == 200
        assert isinstance(response.json, dict)
        for key in response.json.keys():
            assert response.json[key] == getattr(LawyerModel.query.get(1), key)

    @pytest.mark.lawyer
    def test_update_lawyer(self):
        data = {
            "name": "update_lawyer",
            "username": "update_username",
            "email": "update_email",
            "password": "update_password"
        }
        sign_in = self.test_signin_admin()
        response = self.client.put(
            url_for("lawyer.update_lawyer", lawyer_id=1),
            headers={
                "Authorization": "Bearer " + sign_in.json["access_token"]},
            json=data,
        )
        assert response.status_code == 200
        assert isinstance(response.json, dict)
        assert LawyerModel.query.count() == 1
        for key in response.json.keys():
            assert response.json[key] == getattr(LawyerModel.query.get(1), key)

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
        assert LawyerModel.query.count() == 2
        sign_in = self.test_signin_admin()
        response = self.client.delete(
            url_for("lawyer.delete_lawyer", lawyer_id=2),
            headers={"Authorization": "Bearer " + sign_in.json["access_token"]}
        )
        assert response.status_code == 204
        assert LawyerModel.query.count() == 1


if __name__ == "__main__":
    unittest.main()
