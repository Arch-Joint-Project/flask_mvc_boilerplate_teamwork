import pytest
from tests import BaseTestCase
from tests.test_admin_views import TestAdminViews

t = TestAdminViews()
b = BaseTestCase()


@pytest.fixture(scope="class")
def admin_signin(request):
    # # client = b.create_app().test_client()
    # data = {
    #     "username": "test_admin_username",
    #     "password": "test_admin_password"
    # }
    # cl = t.c
    # response = create_app("config.TestingConfig").test_client().post(url_for("admin.admin_create"))
    # # s = TestAdminViews().test_signin_admin()
    # # request.cls.s = s
    # print("this is the ", cl)
    # a = t.test_signin_admin()
    # print(t)
    yield
    # print(f'this is s {s}')
    # return s
    # return s
    # data = {
    #     "username": "test_admin_username",
    #     "password": "test_admin_password"
    # }
    # client = create_app().test_client()
    # response = client.post(url_for("admin.admin_signin"),
    #                             json=data)
    # print(response.status_code)
    # return response.json.values()
