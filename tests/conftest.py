import pytest
from base64 import b64encode
from flask_testing import TestCase
from werkzeug.test import Client
from tests import BaseTestCase
from app import create_app


@pytest.fixture(scope='class')
def admin_signin():
    data = {
        "username": "test_admin_username",
        "password": "test_admin_password"
    }
    client = create_app().test_client()
    response = client.post("http://localhost:5000/api/admin/signin",
                                json=data)
    return response
