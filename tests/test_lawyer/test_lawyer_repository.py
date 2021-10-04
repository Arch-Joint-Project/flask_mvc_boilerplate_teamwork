from app.repositories import LawyerRepository
from tests import BaseTestCase
import pytest
from app.models import LawyerModel
import unittest

NEW_LAWYER = {
    "admin_id": 1,
    "name": "new_lawyer",
    "username": "new_username",
    "email": "new_email",
    "password": "new_password"
}
UPDATE_LAWYER_INFO = {
    "name": "update_admin",
    "username": "update_admin_username",
    "email": "update_admin_email",
    "password": "update_admin_password"
}


class TestLawyerRepository(BaseTestCase):
    @pytest.mark.lawyer
    def test_index(self):
        get_all_lawyers = LawyerRepository(self.redis).index()
        self.assertEqual(LawyerModel.query.count(), 1)
        self.assertIsInstance(get_all_lawyers, list)
        self.assertEqual(len(get_all_lawyers), 1)
        self.assertIsInstance(get_all_lawyers[0], LawyerModel)
        self.assertEqual(get_all_lawyers[0].id, 1)
        self.assertEqual(self.lawyer_model.name, get_all_lawyers[0].name)
        self.assertEqual(self.lawyer_model.email, get_all_lawyers[0].email)
        self.assertEqual(self.lawyer_model.username, get_all_lawyers[0].username)
        self.assertEqual(self.lawyer_model.password, get_all_lawyers[0].password)

    @pytest.mark.lawyer
    def test_create(self):
        create_new_lawyer = LawyerRepository(self.redis).create(NEW_LAWYER)
        self.assertEqual(LawyerModel.query.count(), 2)
        self.assertIsInstance(create_new_lawyer, LawyerModel)
        self.assertEqual(create_new_lawyer.id, 2)
        self.assertEqual(NEW_LAWYER["name"], create_new_lawyer.name)
        self.assertEqual(NEW_LAWYER["email"], create_new_lawyer.email)
        self.assertEqual(NEW_LAWYER["username"], create_new_lawyer.username)
        self.assertTrue(
            create_new_lawyer.verify_password(NEW_LAWYER["password"]))

    @pytest.mark.lawyer
    def test_find_by_id(self):
        find_lawyer_by_id = LawyerRepository(self.redis).find_by_id(1)
        self.assertEqual(LawyerModel.query.count(), 1)
        self.assertIsInstance(find_lawyer_by_id, LawyerModel)
        self.assertEqual(find_lawyer_by_id.id, 1)
        self.assertEqual(self.lawyer_model.name, find_lawyer_by_id.name)
        self.assertEqual(self.lawyer_model.email, find_lawyer_by_id.email)
        self.assertEqual(self.lawyer_model.username, find_lawyer_by_id.username)
        self.assertEqual(self.lawyer_model.password, find_lawyer_by_id.password)

    @pytest.mark.lawyer
    def test_update_by_id(self):
        update_admin = LawyerRepository(self.redis).update_by_id(1, UPDATE_LAWYER_INFO)
        self.assertEqual(LawyerModel.query.count(), 1)
        self.assertIsInstance(update_admin, LawyerModel)
        self.assertEqual(update_admin.id, 1)
        self.assertEqual(update_admin.name, UPDATE_LAWYER_INFO["name"])
        self.assertEqual(update_admin.email, UPDATE_LAWYER_INFO["email"])
        self.assertEqual(update_admin.username, UPDATE_LAWYER_INFO["username"])
        self.assertTrue(update_admin.verify_password(UPDATE_LAWYER_INFO["password"]))

    @pytest.mark.lawyer
    def test_delete(self):
        LawyerRepository(self.redis).create(NEW_LAWYER)
        self.assertEqual(LawyerModel.query.count(), 2)
        delete_lawyer = LawyerRepository(self.redis).delete(2)
        self.assertEqual(LawyerModel.query.count(), 1)
        self.assertEqual(delete_lawyer, None)


if __name__ == "__main__":
    unittest.main()
