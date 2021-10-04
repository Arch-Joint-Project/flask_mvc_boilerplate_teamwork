from app.repositories import AdminRepository
from tests import BaseTestCase
import pytest
from app.models import AdminModel
import unittest

NEW_ADMIN_DATA = {
    "name": "new_admin",
    "username": "new_admin_username",
    "email": "new_admin_email",
    "password": "new_admin_password"
}
UPDATE_ADMIN_INFO = {
    "name": "update_admin",
    "username": "update_admin_username",
    "email": "update_admin_email",
    "password": "update_admin_password"
}


class TestAdminRepository(BaseTestCase):
    @pytest.mark.admin
    def test_index(self):
        get_all_admins = AdminRepository(self.redis).index()
        self.assertEqual(AdminModel.query.count(), 1)
        self.assertIsInstance(get_all_admins, list)
        self.assertEqual(len(get_all_admins), 1)
        self.assertIsInstance(get_all_admins[0], AdminModel)
        self.assertEqual(get_all_admins[0].id, 1)
        self.assertEqual(self.admin_model.name, get_all_admins[0].name)
        self.assertEqual(self.admin_model.email, get_all_admins[0].email)
        self.assertEqual(self.admin_model.username, get_all_admins[0].username)
        self.assertEqual(self.admin_model.password, get_all_admins[0].password)

    @pytest.mark.admin
    def test_create(self):
        create_new_admin = AdminRepository(self.redis).create(NEW_ADMIN_DATA)
        self.assertEqual(AdminModel.query.count(), 2)
        self.assertIsInstance(create_new_admin, AdminModel)
        self.assertEqual(create_new_admin.id, 2)
        self.assertEqual(NEW_ADMIN_DATA["name"], create_new_admin.name)
        self.assertEqual(NEW_ADMIN_DATA["email"], create_new_admin.email)
        self.assertEqual(NEW_ADMIN_DATA["username"], create_new_admin.username)
        self.assertTrue(
            create_new_admin.verify_password(NEW_ADMIN_DATA["password"]))

    @pytest.mark.admin
    def test_find_by_id(self):
        find_admin_by_id = AdminRepository(self.redis).find_by_id(1)
        self.assertEqual(AdminModel.query.count(), 1)
        self.assertIsInstance(find_admin_by_id, AdminModel)
        self.assertEqual(find_admin_by_id.id, 1)
        self.assertEqual(find_admin_by_id.name, self.admin_model.name)
        self.assertEqual(find_admin_by_id.email, self.admin_model.email)
        self.assertEqual(find_admin_by_id.username, self.admin_model.username)
        self.assertEqual(find_admin_by_id.password, self.admin_model.password)

    @pytest.mark.admin
    def test_update_by_id(self):
        update_admin = AdminRepository(self.redis).update_by_id(1, UPDATE_ADMIN_INFO)
        self.assertEqual(AdminModel.query.count(), 1)
        self.assertIsInstance(update_admin, AdminModel)
        self.assertEqual(update_admin.id, 1)
        self.assertEqual(update_admin.name, UPDATE_ADMIN_INFO["name"])
        self.assertEqual(update_admin.email, UPDATE_ADMIN_INFO["email"])
        self.assertEqual(update_admin.username, UPDATE_ADMIN_INFO["username"])
        self.assertTrue(update_admin.verify_password(UPDATE_ADMIN_INFO["password"]))

    @pytest.mark.admin
    def test_delete(self):
        AdminRepository(self.redis).create(NEW_ADMIN_DATA)
        self.assertEqual(AdminModel.query.count(), 2)
        delete_admin = AdminRepository(self.redis).delete(2)
        self.assertEqual(AdminModel.query.count(), 1)
        self.assertEqual(delete_admin, None)


if __name__ == "__main__":
    unittest.main()
