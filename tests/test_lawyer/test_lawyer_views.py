import unittest
from tests import BaseTestCase, SharedResponse
from app.models import LawyerModel
from app import db
import pytest
from flask import url_for

NEW_LAWYER = {
    "name": "new_lawyer",
    "username": "new_username",
    "email": "new_email",
    "password": "new_password"
}
UPDATE_LAWYER_INFO = {
    "name": "update_lawyer",
    "username": "update_username",
    "email": "update_email",
    "password": "update_password"
}


class TestLawyerViews(BaseTestCase):
    @pytest.mark.lawyer
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

    @pytest.mark.lawyer
    def test_signin_lawyer(self):
        invalid_lawyer_info = {
            "username": "test_admin_usname",
            "password": "test_admin_password"
        }
        invalid_lawyer_info_response = self.client.post(
            url_for("lawyer.signin_lawyer"), json=invalid_lawyer_info)
        self.assert200(invalid_lawyer_info_response)
        self.assertIsInstance(invalid_lawyer_info_response.json, dict)
        self.assertEqual(self.shared_responses.signin_invalid_credentials(),
                         invalid_lawyer_info_response.json)
        valid_lawyer_info = {
            "username": self.lawyer["username"],
            "password": self.lawyer["password"]
        }
        valid_lawyer_info_response = self.client.post(
            url_for("lawyer.signin_lawyer"),
            json=valid_lawyer_info)
        self.assert200(valid_lawyer_info_response)
        self.assertIsInstance(valid_lawyer_info_response.json, dict)
        self.assertEqual(
            self.shared_responses.signin_valid_credentials().keys(),
            valid_lawyer_info_response.json.keys())
        return valid_lawyer_info_response

    @pytest.mark.lawyer
    def test_create_lawyer(self):
        admin_sign_in = self.test_signin_admin()
        lawyer_sign_in = self.test_signin_lawyer()
        no_token_response = self.client.get(url_for("lawyer.create_lawyer"))
        self.assert401(no_token_response)
        self.assertIsInstance(no_token_response.json, dict)
        self.assertEqual(no_token_response.json,
                         self.shared_responses.missing_token_authentication())
        wrong_access_token_response = self.client.post(
            url_for("lawyer.create_lawyer"),
            headers={"Authorization": "Bearer " +
                                      lawyer_sign_in.json["access_token"]
                     }, json=NEW_LAWYER
        )
        self.assert401(wrong_access_token_response)
        self.assertIsInstance(wrong_access_token_response.json, dict)
        self.assertEqual(wrong_access_token_response.json,
                         self.shared_responses.unauthorize_operation())
        right_access_token_response = self.client.post(
            url_for("lawyer.create_lawyer"),
            headers={"Authorization": "Bearer "
                                      + admin_sign_in.json["access_token"]
                     }, json=NEW_LAWYER
        )
        self.assertEqual(right_access_token_response.status_code, 201)
        self.assertEqual(LawyerModel.query.count(), 2)
        self.assertIsInstance(right_access_token_response.json, dict)
        for key in right_access_token_response.json.keys():
            self.assertEqual(right_access_token_response.json[key],
                             getattr(LawyerModel.query.get(2), key))

    @pytest.mark.lawyer
    def test_view_lawyers(self):
        sign_in = self.test_signin_admin()
        response = self.client.get(
            url_for("lawyer.view_lawyers"),
            headers={
                "Authorization": "Bearer " + sign_in.json["access_token"]})
        self.assertEqual(LawyerModel.query.count(), 1)
        self.assert200(response)
        self.assertIsInstance(response.json, list)
        self.assertIsInstance(response.json[0], dict)
        for key in response.json[0].keys():
            self.assertEqual(response.json[0][key],
                             getattr(LawyerModel.query.get(1), key))

    @pytest.mark.lawyer
    def test_view_lawyer(self):
        sign_in = self.test_signin_admin()
        resource_unavailable_response = self.client.get(
            url_for("lawyer.view_lawyer", lawyer_id=2),
            headers={"Authorization": "Bearer " + sign_in.json["access_token"]}
        )
        self.assert404(resource_unavailable_response)
        self.assertIsInstance(resource_unavailable_response.json, dict)
        self.assertEqual(resource_unavailable_response.json,
                         self.shared_responses.resource_unavailable())
        resource_available_response = self.client.get(
            url_for("lawyer.view_lawyer", lawyer_id=1),
            headers={"Authorization": "Bearer " + sign_in.json["access_token"]}
        )
        self.assertEqual(LawyerModel.query.count(), 1)
        self.assert200(resource_available_response)
        self.assertIsInstance(resource_available_response.json, dict)
        for key in resource_available_response.json.keys():
            self.assertEqual(resource_available_response.json[key],
                             getattr(LawyerModel.query.get(1), key))

    @pytest.mark.lawyer
    def test_update_lawyer(self):
        sign_in = self.test_signin_admin()
        update_lawyer_response = self.client.put(
            url_for("lawyer.update_lawyer", lawyer_id=1),
            headers={"Authorization": "Bearer " + sign_in.json["access_token"]}
            , json=UPDATE_LAWYER_INFO
        )
        self.assertEqual(LawyerModel.query.count(), 1)
        self.assert200(update_lawyer_response)
        self.assertIsInstance(update_lawyer_response.json, dict)
        for key in update_lawyer_response.json.keys():
            self.assertEqual(update_lawyer_response.json[key],
                             getattr(LawyerModel.query.get(1), key))

    @pytest.mark.lawyer
    def test_delete_lawyer(self):
        sign_in = self.test_signin_admin()
        new_lawyer_info = NEW_LAWYER.copy()
        new_lawyer_info["admin_id"] = 1
        new_lawyer = LawyerModel(**new_lawyer_info)
        db.session.add(new_lawyer)
        db.session.commit()
        self.assertEqual(LawyerModel.query.count(), 2)
        delete_lawyer_response = self.client.delete(
            url_for("lawyer.delete_lawyer", lawyer_id=2),
            headers={"Authorization": "Bearer " + sign_in.json["access_token"]}
        )
        self.assertEqual(delete_lawyer_response.status_code, 204)
        self.assertEqual(LawyerModel.query.count(), 1)

    @pytest.mark.lawyer
    def test_refresh_token(self):
        sign_in = self.test_signin_lawyer()
        access_token_response = self.client.get(
            url_for("lawyer.refresh_access_token"),
            headers={"Authorization": "Bearer " + sign_in.json["access_token"]}
        )
        self.assert401(access_token_response)
        self.assertEqual(access_token_response.json,
                         self.shared_responses.refresh_token_required())
        refresh_token_response = self.client.get(
            url_for("lawyer.refresh_access_token"),
            headers={
                "Authorization": "Bearer " + sign_in.json["refresh_token"]}
        )
        self.assert200(refresh_token_response)
        self.assertEqual(refresh_token_response.json.keys(),
                         self.shared_responses.signin_valid_credentials().keys())


if __name__ == "__main__":
    unittest.main()
