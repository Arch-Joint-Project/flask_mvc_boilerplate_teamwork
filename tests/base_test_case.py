from flask_testing import TestCase

from app import create_app


class BaseTestCase(TestCase):
    def create_app(self):

        app = create_app()
        app.config.from_object("config.TestingConfig")
        return app

    def setUp(self):
        """
        Will be called before every test
        """

    def tearDown(self):
        """
        Will be called after every test
        """
