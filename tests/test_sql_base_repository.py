from app.definitions.repository.base import SQLBaseRepository
from .base_test_case import BaseTestCase
from app.models import User

TEST_EMAIL="john@example.com"


class SQLBaseRepositoryTestCase(BaseTestCase):
    def test_create_data(self):
        base_repository = SQLBaseRepository()
        base_repository.model = User
        user = base_repository.create(
            {
                "name": "john",
                "email": TEST_EMAIL
            }
        )
        self.assertEqual(user.name, "john")

    def test_find_data(self):
        base_repository = SQLBaseRepository()
        base_repository.model = User

        user = base_repository.create(
            {
                "name": "john",
                "email": TEST_EMAIL
            }
        )
        self.assertEqual(user.name, "john")

        search_user = base_repository.find_by_id(user.id)
        self.assertEqual(search_user.name, "john")

    def test_update_data(self):
        base_repository = SQLBaseRepository()
        base_repository.model = User

        user = base_repository.create(
            {
                "name": "john",
                "email": TEST_EMAIL
            }
        )
        self.assertEqual(user.name, "john")

        updated_user = base_repository.update_by_id(user.id, {
            "name": "jack"
        })
        self.assertEqual(updated_user.name, "jack")

    def test_delete_data(self):
        base_repository = SQLBaseRepository()
        base_repository.model = User

        user = base_repository.create(
            {
                "name": "john",
                "email": TEST_EMAIL
            }
        )
        self.assertEqual(user.name, "john")
        search_user = base_repository.find_by_id(user.id)
        self.assertEqual(search_user.name, "john")

        base_repository.delete(user.id)
        search_user = base_repository.find_by_id(user.id)
        self.assertFalse(search_user)
