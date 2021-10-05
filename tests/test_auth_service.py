from app.controllers import LawyerController
from app.repositories import LawyerRepository
from tests import BaseTestCase
import pytest
from app.models import LawyerModel, AdminModel
import unittest
from app.core.service_result import ServiceResult
from app.services import AuthService
from jwt import InvalidTokenError, PyJWTError


class TestAuthService(BaseTestCase):
    auth = AuthService()

    @pytest.mark.admin
    def test_create_token(self):
        token = self.auth.create_token(self.admin_model.id, self.admin_model.role)
        self.assertIsInstance(token, list)
        self.assertEqual(len(token), 2)
        return token

    @pytest.mark.admin
    def test_decode_token(self):
        token = self.auth.create_token(self.admin_model.id, self.admin_model.role)
        access_token, refresh_token = token
        access_payload = self.auth.decode_token(access_token)
        refresh_payload = self.auth.decode_token(refresh_token)
        self.assertIsInstance(access_payload, dict)
        self.assertIsInstance(refresh_payload, dict)
        self.assertEqual(self.admin_model.id, access_payload["id"])
        self.assertEqual(self.admin_model.role, access_payload["role"])
        self.assertEqual("access_token", access_payload["grant_type"])
        self.assertEqual("refresh_token", refresh_payload["grant_type"])
        return access_payload, refresh_payload

    @pytest.mark.admin
    def test_check_token_type(self):
        access_payload, refresh_payload = self.test_decode_token()
        self.assertIsNone(self.auth.check_token_type(access_payload))
        self.assertEqual(
            self.auth.check_token_type(access_payload, refresh_token=True).json
            , self.shared_responses.refresh_token_required()
        )
        self.assertIsNone(
            self.auth.check_token_type(refresh_payload, refresh_token=True)
        )
        self.assertEqual(
            self.auth.check_token_type(refresh_payload).json,
            self.shared_responses.access_token_required()
        )

    @pytest.mark.admin
    def test_check_access_role(self):
        access_payload, refresh_payload = self.test_decode_token()
        self.assertIsNone(self.auth.check_access_role(access_payload, [self.admin_model.role]))
        self.assertEqual(
            self.auth.check_access_role(access_payload, [self.lawyer_model.role]).json
            , self.shared_responses.unauthorize_operation()
        )
        self.assertEqual(
            self.auth.check_access_role(access_payload, []).json
            , self.shared_responses.unauthorize_operation()
        )


if __name__ == "__main__":
    unittest.main()
