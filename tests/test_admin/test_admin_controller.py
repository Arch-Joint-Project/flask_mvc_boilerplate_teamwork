from app.controllers import AdminController
from app.repositories import AdminRepository
from tests import BaseTestCase
import pytest
from app.models import AdminModel
import unittest
from app.core.service_result import ServiceResult


class TestAdminController(BaseTestCase):
    @pytest.mark.admin
    def test_index(self):
        get_all_admins = AdminController(AdminRepository(self.redis)).index()
        self.assertEqual(AdminModel.query.count(), 1)
        self.assertIsInstance(get_all_admins, ServiceResult)
        self.assertTrue(get_all_admins.success)
        self.assert200(get_all_admins.data)
        self.assertEqual(get_all_admins.exception_case, None)

    @pytest.mark.admin
    def test_create(self):
        new_admin_data = {
            "name": "new_admin",
            "username": "new_admin_username",
            "email": "new_admin_email",
            "password": "new_admin_password"
        }
        create_new_admin = AdminController(AdminRepository(self.redis)).create(new_admin_data)
        self.assertEqual(AdminModel.query.count(), 2)
        self.assertIsInstance(create_new_admin, ServiceResult)
        self.assertTrue(create_new_admin.success)
        self.assertEqual(create_new_admin.data.status_code, 201)
        self.assertEqual(create_new_admin.exception_case, None)

    @pytest.mark.admin
    def test_find_by_id(self):
        find_admin_by_id = AdminController(AdminRepository(self.redis)).find_by_id(1)
        self.assertEqual(AdminModel.query.count(), 1)
        self.assertIsInstance(find_admin_by_id, ServiceResult)
        self.assertTrue(find_admin_by_id.success)
        self.assert200(find_admin_by_id.data)
        self.assertEqual(find_admin_by_id.exception_case, None)

    @pytest.mark.admin
    def test_update_by_id(self):
        update_admin_info = {
            "name": "update_admin",
            "username": "update_admin_username",
            "email": "update_admin_email",
            "password": "update_admin_password"
        }
        update_admin = AdminController(AdminRepository(self.redis)).update_by_id(1, update_admin_info)
        self.assertEqual(AdminModel.query.count(), 1)
        self.assertIsInstance(update_admin, ServiceResult)
        self.assertTrue(update_admin.success)
        self.assert200(update_admin.data)
        self.assertEqual(update_admin.exception_case, None)

    @pytest.mark.admin
    def test_delete(self):
        add_new_admin = {
            "name": "new_admin",
            "username": "new_username",
            "email": "new_password",
            "password": "new_password"
        }
        AdminController(AdminRepository(self.redis)).create(add_new_admin)
        self.assertEqual(AdminModel.query.count(), 2)
        delete_admin = AdminController(AdminRepository(self.redis)).delete(2)
        self.assertEqual(AdminModel.query.count(), 1)
        self.assertIsInstance(delete_admin, ServiceResult)
        self.assertTrue(delete_admin.success)
        self.assertEqual(delete_admin.data.status_code, 204)
        self.assertEqual(delete_admin.exception_case, None)

    @pytest.mark.admin
    def test_sign_in(self):
        admin_info = {
            "username": self.admin.get("username"),
            "password": self.admin.get("password")
        }
        admin_sign_in = AdminController(AdminRepository(self.redis)).sign_in(admin_info)
        self.assert200(admin_sign_in)
        self.assertIsInstance(admin_sign_in.json, dict)
        self.assertEqual(len(admin_sign_in.json), len(self.shared_responses.signin_valid_credentials()))
        self.assertEqual(admin_sign_in.json.keys(), self.shared_responses.signin_valid_credentials().keys())


if __name__ == "__main__":
    unittest.main()
