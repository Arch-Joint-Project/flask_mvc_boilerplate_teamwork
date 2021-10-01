import fakeredis
from werkzeug.security import generate_password_hash, check_password_hash
from app.repositories import AdminRepository
from tests import BaseTestCase
from unittest.mock import patch
from app.services import RedisService
import pytest
from app.models import AdminModel


#
# patcher = patch("app.services.redis_service.redis_conn", fakeredis.FakeStrictRedis())
# redis = patcher.start()
# # redis_service = patch("app.services.redis_service.redis_conn")
# # print(redis_service)

# admin_repository = AdminRepository(redis)


@pytest.mark.usefixtures("base_test_case_setup_requirement")
class TestAdminRepository(BaseTestCase):
    # r = AdminRepository()
    @pytest.mark.admin
    def test_index(self):
        get_all_admin = AdminRepository(self.redis).index()
        self.assertEqual(AdminModel.query.count(), 1)
        self.assertIsInstance(get_all_admin, list)
        self.assertEqual(len(get_all_admin), 1)
        self.assertIsInstance(get_all_admin[0], AdminModel)
        self.assertTrue(
            get_all_admin[0].verify_password(self.init_admin_info["password"]))
        self.init_admin_info.pop("password")
        for key in self.init_admin_info.keys():
            self.assertEqual(self.init_admin_info[key],
                             getattr(get_all_admin[0], key))

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
        self.assertTrue(new_admin.verify_password(admin_data.get("password")))
        admin_data.pop("password")
        for key in admin_data:
            self.assertEqual(admin_data[key], getattr(new_admin, key))

    @pytest.mark.admin
    def test_find_by_id(self):
        find_admin = AdminRepository(self.redis).find_by_id(1)
        print(find_admin.hash_password)
        self.assertEqual(AdminModel.query.count(), 1)
        self.assertIsInstance(find_admin, AdminModel)
        self.assertEqual(find_admin.id, 1)
        self.assertTrue(
            find_admin.verify_password(self.init_admin_info.get("password")))
        self.init_admin_info.pop("password")
        for key in self.init_admin_info:
            self.assertEqual(self.init_admin_info[key],
                             getattr(find_admin, key))

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
        # self.assertTrue(update_admin.verify_password(new_info["password"]))
        new_info.pop("password")
        for key in new_info.keys():
            self.assertEqual(new_info[key], getattr(update_admin, key))

    @pytest.mark.active
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
