import os
from tests import BaseTestCase
import pytest

# basedir = os.path.abspath(os.path.dirname(__file__))
# the_basedir = os.path.abspath(os.path.join(__file__, os.pardir))
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestAppConfig(BaseTestCase):
    @pytest.mark.app
    def test_app_config(self):
        self.assertTrue(self.create_app().config["DEBUG"])
        self.assertEqual(
            self.create_app().config["SQLALCHEMY_DATABASE_URI"],
            "sqlite:///" + os.path.join(basedir, "test") +
            ".db?check_same_thread=False"
        )
        self.assertTrue(self.create_app().config["TESTING"])
        self.assertTrue(self.create_app().config["DEVELOPMENT"])
        self.assertEqual(self.create_app().config["SECRET_KEY"], "thisisthesecretkey")
