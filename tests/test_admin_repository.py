from app.repositories import AdminRepository
from tests import BaseTestCase
import pytest
from app.models import AdminModel
from .test_responses import SharedResponse
from werkzeug.security import generate_password_hash, check_password_hash


@pytest.mark.usefixtures("initial_data")
class TestAdminRepository(BaseTestCase):
    @pytest.mark.admin
    def test_index(self):
        get_all_admin = AdminRepository(self.redis).index()
        self.assertEqual(AdminModel.query.count(), 1)
        self.assertIsInstance(get_all_admin, list)
        self.assertEqual(len(get_all_admin), 1)
        self.assertIsInstance(get_all_admin[0], AdminModel)
        self.assertEqual(get_all_admin[0].id, 1)
        # print(check_password_hash(get_all_admin[0].hash_password, self.admin_data["password"]))

    @pytest.mark.admin
    def test_create(self):
        admin_data = {
            "name": "new_admin",
            "username": "new_admin_username",
            "email": "new_admin_email",
            "password": "new_admin_password"
        }
        new_admin = AdminRepository(self.redis).create(admin_data)
        self.assertIsInstance(new_admin, AdminModel)
        self.assertEqual(AdminModel.query.count(), 2)
        self.assertEqual(new_admin.id, 2)

    @pytest.mark.admin
    def test_find_by_id(self):
        # print("new self.admin", self.admin_info)
        find_admin = AdminRepository(self.redis).find_by_id(1)
        self.assertEqual(AdminModel.query.count(), 1)
        self.assertIsInstance(find_admin, AdminModel)
        self.assertEqual(find_admin.id, 1)

    @pytest.mark.admin
    def test_update_by_id(self):
        new_info = {
            "name": "update_admin",
            "username": "update_admin_username",
            "email": "update_admin_email",
            "password": "update_admin_password"
        }
        update_admin = AdminRepository(self.redis).update_by_id(1, new_info)
        self.assertEqual(AdminModel.query.count(), 1)
        self.assertIsInstance(update_admin, AdminModel)
        self.assertEqual(update_admin.id, 1)

    @pytest.mark.admin
    def test_delete(self):
        new_admin = {
            "name": "new_admin",
            "username": "new_username",
            "email": "new_password",
            "password": "new_password"
        }
        AdminRepository(self.redis).create(new_admin)
        self.assertEqual(AdminModel.query.count(), 2)
        delete_admin = AdminRepository(self.redis).delete(2)
        self.assertEqual(AdminModel.query.count(), 1)
        self.assertEqual(delete_admin, None)
