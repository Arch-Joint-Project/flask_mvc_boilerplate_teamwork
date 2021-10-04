from app.controllers import LawyerController
from app.repositories import LawyerRepository
from tests import BaseTestCase
import pytest
from app.models import LawyerModel
import unittest
from app.core.service_result import ServiceResult

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


class TestLawyerController(BaseTestCase):
    @pytest.mark.lawyer
    def test_index(self):
        get_all_lawyers = LawyerController(LawyerRepository(self.redis)).index()
        self.assertEqual(LawyerModel.query.count(), 1)
        self.assertIsInstance(get_all_lawyers, ServiceResult)
        self.assertTrue(get_all_lawyers.success)
        self.assert200(get_all_lawyers.data)
        self.assertEqual(get_all_lawyers.exception_case, None)

    @pytest.mark.lawyer
    def test_create(self):
        create_new_lawyer = LawyerController(
            LawyerRepository(self.redis)).create(1, NEW_LAWYER)
        self.assertEqual(LawyerModel.query.count(), 2)
        self.assertIsInstance(create_new_lawyer, ServiceResult)
        self.assertTrue(create_new_lawyer.success)
        self.assertEqual(create_new_lawyer.data.status_code, 201)
        self.assertEqual(create_new_lawyer.exception_case, None)

    @pytest.mark.lawyer
    def test_find_by_id(self):
        find_lawyer_by_id = LawyerController(LawyerRepository(self.redis)).find_by_id(1)
        self.assertEqual(LawyerModel.query.count(), 1)
        self.assertIsInstance(find_lawyer_by_id, ServiceResult)
        self.assertTrue(find_lawyer_by_id.success)
        self.assert200(find_lawyer_by_id.data)
        self.assertEqual(find_lawyer_by_id.exception_case, None)

    @pytest.mark.lawyer
    def test_update_by_id(self):
        update_lawyer = LawyerController(
            LawyerRepository(self.redis)).update_by_id(1, UPDATE_LAWYER_INFO)
        self.assertEqual(LawyerModel.query.count(), 1)
        self.assertIsInstance(update_lawyer, ServiceResult)
        self.assertTrue(update_lawyer.success)
        self.assert200(update_lawyer.data)
        self.assertEqual(update_lawyer.exception_case, None)

    @pytest.mark.lawyer
    def test_delete(self):
        LawyerController(LawyerRepository(self.redis)).create(2, NEW_LAWYER)
        self.assertEqual(LawyerModel.query.count(), 2)
        delete_lawyer = LawyerController(LawyerRepository(self.redis)).delete(2)
        self.assertEqual(LawyerModel.query.count(), 1)
        self.assertIsInstance(delete_lawyer, ServiceResult)
        self.assertTrue(delete_lawyer.success)
        self.assertEqual(delete_lawyer.data.status_code, 204)
        self.assertEqual(delete_lawyer.exception_case, None)

    @pytest.mark.lawyer
    def test_sign_in(self):
        lawyer_info = {
            "username": self.lawyer["username"],
            "password": self.lawyer["password"]
        }
        lawyer_sign_in = LawyerController(LawyerRepository(self.redis)).sign_in(lawyer_info)
        self.assert200(lawyer_sign_in)
        self.assertIsInstance(lawyer_sign_in.json, dict)
        self.assertEqual(lawyer_sign_in.json.keys(),
            self.shared_responses.signin_valid_credentials().keys())


if __name__ == "__main__":
    unittest.main()
