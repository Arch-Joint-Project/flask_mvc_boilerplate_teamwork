from .base_test_case import BaseTestCase
from app.models import UserModel
import unittest

class TestModel(BaseTestCase):
    def test_user_model(self):
        """
        Test number of records in User table
        """
        self.assertEqual(UserModel.qery.count(), 0)


if __name__ == '__main__':
    unittest.main()
