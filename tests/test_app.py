import os
from tests import BaseTestCase

# basedir = os.path.abspath(os.path.dirname(__file__))
# the_basedir = os.path.abspath(os.path.join(__file__, os.pardir))
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print('thisis the ', basedir)


class TestAppConfig(BaseTestCase):
    def test_app_config(self):
        print(self.create_app().config)
        assert self.create_app().config["DEBUG"] == True
        assert self.create_app().config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///" + os.path.join(basedir, "test") + ".db?check_same_thread=False"
        assert self.create_app().config["TESTING"] == True
        assert self.create_app().config["DEVELOPMENT"] == True
        assert self.create_app().config["SECRET_KEY"] == "thisisthesecretkey"