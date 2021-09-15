from random import choice
from tests import BaseTestCase
from app.models import AdminModel, LawyerModel, BillModel
import unittest
import pytest
from app.services import create_token
from flask import url_for

base_test = BaseTestCase()
NO_AUTH_RESPONSE = "Token is missing !!"
ADMIN_SIGNIN_INFO = {
    "username": "test_admin_username",
    "password": "test_admin_password"
}
LAWYER_SIGNIN_INFO = {
    "username": "test_lawyer_username",
    "password": "test_lawyer_password"
}


# @pytest.mark.usefixtures("admin_signin")
class TestAdminViews(BaseTestCase):
    @pytest.mark.admin
    def test_admin_sigin_view(self):
        response = self.client.post(
            url_for("admin.signin_admin"),
            json=ADMIN_SIGNIN_INFO
        )
        assert response.status_code == 200
        assert "token" in response.json.keys()
        response = self.client.get(
            url_for("admin.view_admins"),
            headers={"Authorization": "Bearer " + response.json["token"]}
        )
        assert len(response.json) == 1
        assert "test_admin" in response.json[0].values()

    @pytest.mark.admin
    def test_admin_view(self):
        response = self.client.get(url_for("admin.view_admins"))
        assert response.status_code == 401
        assert NO_AUTH_RESPONSE in response.json.values()
        response = self.client.post(
            url_for("admin.signin_admin"),
            json=ADMIN_SIGNIN_INFO
        )
        assert "token" in response.json.keys()
        response = self.client.get(
            url_for("admin.view_admins"),
            headers={"Authorization": "Bearer " + response.json["token"]}
        )
        assert len(response.json) == 1
        assert "test_admin" in response.json[0].values()

    @pytest.mark.admin
    def test_admin_post(self):
        data = {
            "name": "test_admin",
            "username": "new_username",
            "email": "new_email",
            "password": "test_admin_password"
        }
        response = self.client.post(url_for("admin.create_admin"),
                                    json=data)
        assert response.status_code == 201
        assert AdminModel.query.count() == 2
        assert "new_username" in response.json.values()


# class TestLawyerViews(BaseTestCase):
#     @pytest.mark.active
#     def test_admin_lawyer_post(self):
#         data = {
#             "name": "new_lawyer",
#             "username": "new_username",
#             "email": "new_email",
#             "password": "test_admin_password"
#         }
#         response = self.client.post("http://localhost:5000/api/admin/lawyer",
#                                     json=data)
#         assert response.status_code == 401
#         assert NO_AUTH_RESPONSE in response.json.values()
#         response = self.client.post("http://localhost:5000/api/admin/signin",
#                                     json=ADMIN_SIGNIN_INFO)
#         assert "token" in response.json.keys()
#         response = self.client.post(
#             "http://localhost:5000/api/admin/lawyer",
#             headers={"Authorization": "Bearer " + response.json["token"]},
#             json=data
#         )
#         assert response.status_code == 201
#         assert LawyerModel.query.count() == 2
#         assert "new_username" in response.json.values()
#
#     @pytest.mark.admin
#     def test_admin_lawyer_view(self):
#         response = self.client.get("http://localhost:5000/api/admin/lawyer")
#         assert response.status_code == 401
#         assert "Token is missing !!" in response.json.values()
#         response = self.client.get(
#             "http://localhost:5000/api/admin/lawyer",
#             headers={"Authorization": "Bearer " + create_token(1, "test_admin_username", "test_admin_email")}
#         )
#         assert len(response.json) == 1
#         assert "test_lawyer" in response.json[0].values()
#
#     @pytest.mark.lawyer
#     def test_admin_bill_view(self):
#         response = self.client.get("http://localhost:5000/api/admin/bill")
#         assert NO_AUTH_RESPONSE in response.json.values()
#         response = self.client.get(
#             "http://localhost:5000/api/admin/bill",
#             headers={"Authorization": "Bearer " + create_token(1, "test_admin_username", "test_admin_email")}
#         )
#         assert len(response.json) == 1
#         assert response.json[0]["lawyer_id"] == 1
#
#     #Test Case: #1 - Test that admin cannot access invoice generation route without token.
#     @pytest.mark.invoice
#     def test_admin_access_get_company_invoice_no_token(self):
#         #1.  admin logs into system
#         baseUrl = "http://localhost:5000/api/admin/" # the base url.
#         testRoute = "bill/invoice/test_company_bill" # test route
#         forHeaders = {"Authorization": "Bearer " + ""}  #No token passed.
#         response = self.client.get(baseUrl + testRoute,headers =forHeaders)
#          # the response(GET) from the server should assert to 401 since no token provided.
#         assert response.status_code == 401
#
#     #Test Case #2: - Test that admin cannot access invoice generation route with invalid token.
#     @pytest.mark.invoice
#     def test_admin_access_get_company_invoice_invalid_token(self):
#         #1. admin logs into system
#         baseUrl = "http://localhost:5000/api/admin/"  # the base url.
#         testRoute = "bill/invoice/test_company_bill"  # test route
#         buffer = "abcdefghijklmnopqrstuvwxyz" + "123456789"
#         t = ''.join(choice(buffer) for i in range(len(buffer))) # generate some random strings.
#         invalidToken = create_token(1, "test_admin_username", "test_admin_email") + t # entry of more or less token ==> invalid.
#         forHeaders = {"Authorization": "Bearer " + invalidToken}  # headers.
#         response = self.client.get(
#             baseUrl + testRoute,headers=forHeaders)  # @NOTE: headers where not passed.
#         # the response(GET) from the server should assert to 401 since no token provided.
#         assert response.status_code == 401
#
#     #Test Case: #3 - Confirm that admin can access invoice generation route with the valid token provided.
#     @pytest.mark.invoice
#     def test_admin_can_access_get_company_invoice_with_token_provided(self):
#         # 1. admin logs into system.
#          baseUrl = "http://localhost:5000/api/admin/" # the base url
#          testRoute = "bill/invoice/test_company_bill"  # test route
#          validToken = create_token(1, "test_admin_username", "test_admin_email")
#          forHeaders = {"Authorization":"Bearer " + validToken} # headers.
#          # 2. admin's token get passed.
#          response = self.client.get(baseUrl + testRoute,headers=forHeaders)
#             # the response from the server should be successfully since tokens are passed.
#          assert response.status_code == 200 or 201
#
#     #Test Case: #4 - Confirm that admin can generate invoice
#     @pytest.mark.invoice
#     def test_admin_can_generate_invoice(self):
#         #1. admin logs into system.
#         baseUrl = "http://localhost:5000/api/admin/"  # the base url
#         testRoute = "bill/invoice/test_company_bill"  # test route
#         validToken = create_token(1, "test_admin_username", "test_admin_email")
#         forHeaders = {"Authorization": "Bearer " + validToken}  # headers.
#
#         # 2. admin's token get passed.
#         response = self.client.get(baseUrl + testRoute, headers=forHeaders,)
#         # the response from the server should be successfully since tokens are passed.
#         assert response.status_code == 200 or 201
#
#
#
#
#
#
#
#
#
#

class TestLawyerViews(BaseTestCase):
    @pytest.mark.active
    def test_lawyer_sigin_view(self):
        lawyer_signin = self.client.post(
            url_for("lawyer.signin_lawyer"),
            json=LAWYER_SIGNIN_INFO
        )
        assert lawyer_signin.status_code == 200
        assert "token" in lawyer_signin.json.keys()
        lawyer_response = self.client.get(
            url_for("lawyer.view_lawyers"),
            headers={"Authorization": "Bearer " + lawyer_signin.json["token"]}
        )
        print(lawyer_response.json)
        assert isinstance(lawyer_response.json, dict)
        assert "test_lawyer" in lawyer_response.json.values()
        admin_signin = self.client.post(url_for("admin.signin_admin"),
                                        json=ADMIN_SIGNIN_INFO)
        assert admin_signin.status_code == 200
        assert "token" in admin_signin.json.keys()
        admin_response = self.client.get(
            url_for("lawyer.view_lawyers"),
            headers={"Authorization": "Bearer " + admin_signin.json["token"]}
        )
        print(admin_response.json)
        assert isinstance(admin_response.json, list)
        assert len(admin_response.json) == 1
        assert "test_lawyer" in admin_response.json[0].values()

    @pytest.mark.lawyer
    def test_lawyer_view(self):
        response = self.client.get("http://localhost:5000/api/lawyer/")
        assert response.status_code == 401
        assert NO_AUTH_RESPONSE in response.json.values()
        response = self.client.get(
            "http://localhost:5000/api/lawyer/",
            headers={"Authorization": "Bearer " + create_token(1, "test_lawyer_username", "test_lawyer_email")}
        )
        assert "test_lawyer" in response.json.values()
        assert response.json["id"] == 1

    @pytest.mark.lawyer
    def test_lawyer_bill_view(self):
        response = self.client.get("http://localhost:5000/api/lawyer/bill")
        assert response.status_code == 401
        assert NO_AUTH_RESPONSE in response.json.values()
        response = self.client.get(
            "http://localhost:5000/api/lawyer/bill",
            headers={"Authorization": "Bearer " + create_token(1, "test_lawyer_username", "test_lawyer_email")}
        )
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]["lawyer_id"] == 1

    @pytest.mark.lawyer
    def test_lawyer_company_bill_view(self):
        response = self.client.get(
            "http://localhost:5000/api/lawyer/bill/company/test_bill_company")
        assert response.status_code == 401
        assert NO_AUTH_RESPONSE in response.json.values()
        response = self.client.get(
            "http://localhost:5000/api/lawyer/bill",
            headers={"Authorization": "Bearer " + create_token(1, "test_lawyer_username", "test_lawyer_email")}
        )
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]["lawyer_id"] == 1

    @pytest.mark.lawyer
    def test_lawyer_bill_post(self):
        data = {
            "billable_rate": 300,
            "company": "test_company",
            "date": "2020-09-09",
            "start_time": "08:30",
            "end_time": "08:30"
        }
        response = self.client.post("http://localhost:5000/api/lawyer/bill",
                                    json=data)
        assert response.status_code == 401
        assert NO_AUTH_RESPONSE in response.json.values()
        response = self.client.post(
            "http://localhost:5000/api/lawyer/bill",
            headers={"Authorization": "Bearer " + create_token(1, "test_lawyer_username", "test_lawyer_email")},
            json=data
        )
        assert response.status_code == 201
        assert BillModel.query.count() == 2
        assert "test_company" in response.json.values()

    @pytest.mark.lawyer
    def test_lawyer_bill_update(self):
        query = {
            "company": "test_bill_company"
        }
        data = {
            "billable_rate": 5000,
            "date": "2020-09-09",
            "start_time": "08:30:00",
            "end_time": "08:30:00"
        }
        response = self.client.put("http://localhost:5000/api/lawyer/bill",
                                   json=data, query_string=query)
        assert response.status_code == 401
        assert "Token is missing !!" == response.json["message"]
        response = self.client.put(
            "http://localhost:5000/api/lawyer/bill",
            headers={"Authorization": "Bearer " + create_token(1, "test_lawyer_username", "test_lawyer_email")},
            json=data,
            query_string=query
        )
        assert response.status_code == 200
        assert BillModel.query.count() == 1
        for values in data.values():
            assert values in response.json.values()
        # assert "test_company" in response.json.values()

    @pytest.mark.lawyer
    def test_lawyer_delete_bill_view(self):
        response = self.client.delete(
            "http://localhost:5000/api/lawyer/bill/test_bill_company")
        assert response.status_code == 401
        assert NO_AUTH_RESPONSE in response.json.values()
        response = self.client.delete(
            "http://localhost:5000/api/lawyer/bill/test_bill_company",
            headers={"Authorization": "Bearer " + create_token(1, "test_lawyer_username", "test_lawyer_email")}
        )
        assert response.status_code == 204
        assert BillModel.query.count() == 0

    # Test Case: #1 - Test that admin cannot access invoice generation route without token.
    @pytest.mark.invoice
    def test_admin_access_get_company_invoice_no_token(self):
        # 1.  admin logs into system
        baseUrl = "http://localhost:5000/api/admin/"  # the base url.
        testRoute = "bill/invoice/test_company_bill"  # test route
        forHeaders = {
            "Authorization": "Bearer " + ""}  # No token passed.
        response = self.client.get(baseUrl + testRoute, headers=forHeaders)
        # the response(GET) from the server should assert to 401 since no token provided.
        assert response.status_code == 401

    # Test Case #2: - Test that admin cannot access invoice generation route with invalid token.
    @pytest.mark.invoice
    def test_admin_access_get_company_invoice_invalid_token(self):
        # 1. admin logs into system
        baseUrl = "http://localhost:5000/api/admin/"  # the base url.
        testRoute = "bill/invoice/test_bill_company"  # test route
        buffer = "abcdefghijklmnopqrstuvwxyz" + "123456789"
        t = ''.join(choice(buffer) for i in
                    range(len(buffer)))  # generate some random strings.
        invalidToken = create_token(1, "test_lawyer_username", "test_lawyer_email") + t  # entry of more or less token ==> invalid.
        forHeaders = {
            "Authorization": "Bearer " + invalidToken}  # headers.
        response = self.client.get(
            baseUrl + testRoute,
            headers=forHeaders)  # @NOTE: headers where not passed.
        # the response(GET) from the server should assert to 401 since no token provided.
        assert response.status_code == 401

    # Test Case: #3 - Confirm that admin can access invoice generation route with the valid token provided.
    @pytest.mark.invoice
    def test_admin_can_access_get_company_invoice_with_token_provided(
        self):
        # 1. admin logs into system.
        baseUrl = "http://localhost:5000/api/admin/"  # the base url
        testRoute = "bill/invoice/test_company_bill"  # test route
        validToken = create_token(1, "test_lawyer_username", "test_lawyer_email")
        forHeaders = {"Authorization": "Bearer " + validToken}  # headers.
        # 2. admin's token get passed.
        response = self.client.get(baseUrl + testRoute, headers=forHeaders)
        # the response from the server should be successfully since tokens are passed.
        assert response.status_code == 200 or 201

    # Test Case: #4 - Confirm that admin can generate invoice
    @pytest.mark.invoice
    def test_admin_can_generate_invoice(self):
        # 1. admin logs into system.
        baseUrl = "http://localhost:5000/api/admin/"  # the base url
        testRoute = "bill/invoice/<company>"  # test route
        validToken = create_token(1, "test_lawyer_username", "test_lawyer_email")
        forHeaders = {"Authorization": "Bearer " + validToken}  # headers.

        # 2. admin's token get passed.
        response = self.client.get(baseUrl + testRoute,
                                   headers=forHeaders, )
        # the response from the server should be successfully since tokens are passed.
        assert response.status_code == 200 or 201

        # print the invoice generated.
        return response.json.values()



if __name__ == "__main__":
    unittest.main()
