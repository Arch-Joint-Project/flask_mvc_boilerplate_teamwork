import unittest
from tests import BaseTestCase, CommonResponse
from app.models import AdminModel
from app import db
import pytest
from flask import url_for

common_response = CommonResponse()
# NO_AUTH_RESPONSE = "Token is missing !!"


# @pytest.mark.usefixtures("admin_signin_info")
class TestAdminViews(BaseTestCase):
    @pytest.mark.admin
    def test_signin_admin(self):
        # invalid credentials
        admin_info = {
            "username": "test_admin_usname",
            "password": "test_admin_password"
        }
        response = self.client.post(
            url_for("admin.signin_admin"),
            json=admin_info
        )
        assert response.status_code == 200
        assert len(common_response.signin_invalid_credentials()) == \
               len(response.json)
        assert common_response.signin_invalid_credentials() == \
               response.json
        # valid credentials
        admin_info = {
            "username": "test_admin_username",
            "password": "test_admin_password"
        }
        response = self.client.post(
            url_for("admin.signin_admin"),
            json=admin_info
        )
        assert response.status_code == 200
        assert len(common_response.signin_valid_credentials()) == \
               len(response.json)
        assert common_response.signin_valid_credentials().keys() == \
               response.json.keys()
        print("this is the redis conn", self.redis)
        return response

    @pytest.mark.admin
    def test_create_admin(self):
        data = {
            "name": "create_admin",
            "username": "create_username",
            "email": "create_email",
            "password": "create_password"
        }
        response = self.client.post(url_for("admin.create_admin"), json=data)
        assert response.status_code == 201
        print(response.json)
        assert isinstance(response.json, dict)
        assert AdminModel.query.count() == 2
        for key in response.json.keys():
            assert response.json[key] == getattr(AdminModel.query.get(2), key)

    @pytest.mark.admin
    def test_view_admins(self):
        # test without token
        response = self.client.get(url_for("admin.view_admins"))
        assert response.status_code == 401
        assert len(response.json) == \
               len(common_response.missing_token_authentication())
        assert common_response.missing_token_authentication() == response.json
        # test with invalid token
        sign_in = self.test_signin_admin()
        response = self.client.get(
            url_for("admin.view_admins"),
            headers={"Authorization": "Bearer " + sign_in.json[
                "access_token"] + "dfajl"}
        )
        assert response.status_code == 401
        assert isinstance(response.json, dict)
        assert "error" in response.json.keys()
        # test with valid token
        response = self.client.get(
            url_for("admin.view_admins"),
            headers={"Authorization": "Bearer " + sign_in.json[
                "access_token"]}
        )
        assert response.status_code == 200
        assert isinstance(response.json, list)
        for key in response.json[0].keys():
            assert response.json[0][key] == getattr(AdminModel.query.get(1), key)
            # test with refresh token
        response = self.client.get(
            url_for("admin.view_admins"),
            headers={"Authorization": "Bearer " + sign_in.json[
                "refresh_token"]}
        )
        assert response.status_code == 401
        assert isinstance(response.json, dict)
        assert common_response.access_token_required() == response.json

    @pytest.mark.admin
    def test_view_admin(self):
        sign_in = self.test_signin_admin()
        # unavailable user
        response = self.client.get(
            url_for("admin.view_admin", admin_id=2),
            headers={"Authorization": "Bearer " + sign_in.json["access_token"]}
        )
        assert response.status_code == 404
        assert isinstance(response.json, dict)
        assert common_response.resource_unavailable() == response.json
        # available user
        response = self.client.get(
            url_for("admin.view_admin", admin_id=1),
            headers={"Authorization": "Bearer " + sign_in.json["access_token"]}
        )
        assert response.status_code == 200
        assert isinstance(response.json, dict)
        for key in response.json.keys():
            assert response.json[key] == getattr(AdminModel.query.get(1),
                                                    key)

    @pytest.mark.admin
    def test_update_admin(self):
        data = {
            "name": "update_admin",
            "username": "update_username",
            "email": "update_email",
            "password": "update_password"
        }
        sign_in = self.test_signin_admin()
        response = self.client.put(
            url_for("admin.update_admin", admin_id=1),
            headers={"Authorization": "Bearer " + sign_in.json["access_token"]},
            json=data
        )
        assert response.status_code == 200
        assert isinstance(response.json, dict)
        assert AdminModel.query.count() == 1
        for key in response.json.keys():
            assert response.json[key] == getattr(AdminModel.query.get(1), key)

    @pytest.mark.admin
    def test_delete_admin(self):
        new_admin = AdminModel(
            name="test_delete_admin",
            username="test_delete_admin_username",
            email="test_delete_admin_email",
            password="test_delete_admin_password"
        )
        db.session.add(new_admin)
        db.session.commit()
        assert AdminModel.query.count() == 2
        sign_in = self.test_signin_admin()
        response = self.client.delete(
            url_for("admin.delete_admin", admin_id=2),
            headers={"Authorization": "Bearer " + sign_in.json["access_token"]}
        )
        assert response.status_code == 204
        assert AdminModel.query.count() == 1

    @pytest.mark.admin
    def test_refresh_token(self):
        sign_in = self.test_signin_admin()
        # access token
        response = self.client.get(
            url_for("admin.refresh_access_token"),
            headers={"Authorization": "Bearer " + sign_in.json["access_token"]}
        )
        assert response.status_code == 401
        assert common_response.refresh_token_required() == response.json
        response = self.client.get(
            url_for("admin.refresh_access_token"),
            headers={"Authorization": "Bearer " + sign_in.json["refresh_token"]}
        )
        assert response.status_code == 200
        assert common_response.signin_valid_credentials().keys() == \
               response.json.keys()


if __name__ == "__main__":
    unittest.main()













































#     @pytest.mark.admin
#     def test_admin_lawyer_post(self):
#         data = {
#             "name": "new_lawyer",
#             "username": "new_lawyer_username",
#             "email": "new_lawyer_email",
#             "password": "new_lawyer_password"
#         }
#         # with out authentication
#         response = self.client.post(url_for("lawyer.create_lawyer"),
#                                     json=data)
#         assert response.status_code == 401
#         assert NO_AUTH_RESPONSE in response.json.values()
#         # with authentication
#         sign_in = self.test_admin_sigin_view()
#         response = self.client.post(url_for("lawyer.create_lawyer"),
#             headers={"Authorization": "Bearer " + sign_in.json["token"]},
#             json=data
#         )
#         assert response.status_code == 201
#         assert LawyerModel.query.count() == 2
#         assert "new_lawyer_username" in response.json.values()
#
#     @pytest.mark.admin
#     def test_view_lawyer(self):
#         # no authentication
#         response = self.client.get(url_for("lawyer.view_lawyers"))
#         assert response.status_code == 401
#         assert NO_AUTH_RESPONSE in response.json.values()
#         # with authentication
#         sign_in = self.test_admin_sigin_view()
#         response = self.client.get(url_for("lawyer.view_lawyers"),
#             headers={"Authorization": "Bearer " + sign_in.json["token"]}
#         )
#         print(response.json)
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
# # class TestLawyerViews(BaseTestCase):
# #
# #
# #     #Test Case: #1 - Test that admin cannot access invoice generation route without token.
# #     @pytest.mark.invoice
# #     def test_admin_access_get_company_invoice_no_token(self):
# #         #1.  admin logs into system
# #         baseUrl = "http://localhost:5000/api/admin/" # the base url.
# #         testRoute = "bill/invoice/test_company_bill" # test route
# #         forHeaders = {"Authorization": "Bearer " + ""}  #No token passed.
# #         response = self.client.get(baseUrl + testRoute,headers =forHeaders)
# #          # the response(GET) from the server should assert to 401 since no token provided.
# #         assert response.status_code == 401
# #
# #     #Test Case #2: - Test that admin cannot access invoice generation route with invalid token.
# #     @pytest.mark.invoice
# #     def test_admin_access_get_company_invoice_invalid_token(self):
# #         #1. admin logs into system
# #         baseUrl = "http://localhost:5000/api/admin/"  # the base url.
# #         testRoute = "bill/invoice/test_company_bill"  # test route
# #         buffer = "abcdefghijklmnopqrstuvwxyz" + "123456789"
# #         t = ''.join(choice(buffer) for i in range(len(buffer))) # generate some random strings.
# #         invalidToken = create_token(1, "test_admin_username", "test_admin_email") + t # entry of more or less token ==> invalid.
# #         forHeaders = {"Authorization": "Bearer " + invalidToken}  # headers.
# #         response = self.client.get(
# #             baseUrl + testRoute,headers=forHeaders)  # @NOTE: headers where not passed.
# #         # the response(GET) from the server should assert to 401 since no token provided.
# #         assert response.status_code == 401
# #
# #     #Test Case: #3 - Confirm that admin can access invoice generation route with the valid token provided.
# #     @pytest.mark.invoice
# #     def test_admin_can_access_get_company_invoice_with_token_provided(self):
# #         # 1. admin logs into system.
# #          baseUrl = "http://localhost:5000/api/admin/" # the base url
# #          testRoute = "bill/invoice/test_company_bill"  # test route
# #          validToken = create_token(1, "test_admin_username", "test_admin_email")
# #          forHeaders = {"Authorization":"Bearer " + validToken} # headers.
# #          # 2. admin's token get passed.
# #          response = self.client.get(baseUrl + testRoute,headers=forHeaders)
# #             # the response from the server should be successfully since tokens are passed.
# #          assert response.status_code == 200 or 201
# #
# #     #Test Case: #4 - Confirm that admin can generate invoice
# #     @pytest.mark.invoice
# #     def test_admin_can_generate_invoice(self):
# #         #1. admin logs into system.
# #         baseUrl = "http://localhost:5000/api/admin/"  # the base url
# #         testRoute = "bill/invoice/test_company_bill"  # test route
# #         validToken = create_token(1, "test_admin_username", "test_admin_email")
# #         forHeaders = {"Authorization": "Bearer " + validToken}  # headers.
# #
# #         # 2. admin's token get passed.
# #         response = self.client.get(baseUrl + testRoute, headers=forHeaders,)
# #         # the response from the server should be successfully since tokens are passed.
# #         assert response.status_code == 200 or 201

# class TestLawyerViews(BaseTestCase):
#     @pytest.mark.lawyer
#     def test_lawyer_sigin_view(self):
#         lawyer_signin = self.client.post(
#             url_for("lawyer.signin_lawyer"),
#             json=LAWYER_SIGNIN_INFO
#         )
#         assert lawyer_signin.status_code == 200
#         assert "token" in lawyer_signin.json.keys()
#         lawyer_response = self.client.get(
#             url_for("lawyer.view_lawyers"),
#             headers={"Authorization": "Bearer " + lawyer_signin.json["token"]}
#         )
#         print(lawyer_response.json)
#         assert isinstance(lawyer_response.json, dict)
#         assert "test_lawyer" in lawyer_response.json.values()
#         admin_signin = self.client.post(url_for("admin.signin_admin"),
#                                         json=ADMIN_SIGNIN_INFO)
#         assert admin_signin.status_code == 200
#         assert "token" in admin_signin.json.keys()
#         admin_response = self.client.get(
#             url_for("lawyer.view_lawyers"),
#             headers={"Authorization": "Bearer " + admin_signin.json["token"]}
#         )
#         print(admin_response.json)
#         assert isinstance(admin_response.json, list)
#         assert len(admin_response.json) == 1
#         assert "test_lawyer" in admin_response.json[0].values()
#
#     @pytest.mark.lawyer
#     def test_lawyer_view(self):
#         response = self.client.get("http://localhost:5000/api/lawyer/")
#         assert response.status_code == 401
#         assert NO_AUTH_RESPONSE in response.json.values()
#         response = self.client.get(
#             "http://localhost:5000/api/lawyer/",
#             headers={"Authorization": "Bearer " + create_token(1, "test_lawyer_username", "test_lawyer_email")}
#         )
#         assert "test_lawyer" in response.json.values()
#         assert response.json["id"] == 1
#
#     @pytest.mark.lawyer
#     def test_lawyer_bill_view(self):
#         response = self.client.get("http://localhost:5000/api/lawyer/bill")
#         assert response.status_code == 401
#         assert NO_AUTH_RESPONSE in response.json.values()
#         response = self.client.get(
#             "http://localhost:5000/api/lawyer/bill",
#             headers={"Authorization": "Bearer " + create_token(1, "test_lawyer_username", "test_lawyer_email")}
#         )
#         assert response.status_code == 200
#         assert len(response.json) == 1
#         assert response.json[0]["lawyer_id"] == 1
#
#     @pytest.mark.lawyer
#     def test_lawyer_company_bill_view(self):
#         response = self.client.get(
#             "http://localhost:5000/api/lawyer/bill/company/test_bill_company")
#         assert response.status_code == 401
#         assert NO_AUTH_RESPONSE in response.json.values()
#         response = self.client.get(
#             "http://localhost:5000/api/lawyer/bill",
#             headers={"Authorization": "Bearer " + create_token(1, "test_lawyer_username", "test_lawyer_email")}
#         )
#         assert response.status_code == 200
#         assert len(response.json) == 1
#         assert response.json[0]["lawyer_id"] == 1
#
#     @pytest.mark.lawyer
#     def test_lawyer_bill_post(self):
#         data = {
#             "billable_rate": 300,
#             "company": "test_company",
#             "date": "2020-09-09",
#             "start_time": "08:30",
#             "end_time": "08:30"
#         }
#         response = self.client.post("http://localhost:5000/api/lawyer/bill",
#                                     json=data)
#         assert response.status_code == 401
#         assert NO_AUTH_RESPONSE in response.json.values()
#         response = self.client.post(
#             "http://localhost:5000/api/lawyer/bill",
#             headers={"Authorization": "Bearer " + create_token(1, "test_lawyer_username", "test_lawyer_email")},
#             json=data
#         )
#         assert response.status_code == 201
#         assert BillModel.query.count() == 2
#         assert "test_company" in response.json.values()
#
#     @pytest.mark.lawyer
#     def test_lawyer_bill_update(self):
#         query = {
#             "company": "test_bill_company"
#         }
#         data = {
#             "billable_rate": 5000,
#             "date": "2020-09-09",
#             "start_time": "08:30:00",
#             "end_time": "08:30:00"
#         }
#         response = self.client.put("http://localhost:5000/api/lawyer/bill",
#                                    json=data, query_string=query)
#         assert response.status_code == 401
#         assert "Token is missing !!" == response.json["message"]
#         response = self.client.put(
#             "http://localhost:5000/api/lawyer/bill",
#             headers={"Authorization": "Bearer " + create_token(1, "test_lawyer_username", "test_lawyer_email")},
#             json=data,
#             query_string=query
#         )
#         assert response.status_code == 200
#         assert BillModel.query.count() == 1
#         for values in data.values():
#             assert values in response.json.values()
#         # assert "test_company" in response.json.values()
#
#     @pytest.mark.lawyer
#     def test_lawyer_delete_bill_view(self):
#         response = self.client.delete(
#             "http://localhost:5000/api/lawyer/bill/test_bill_company")
#         assert response.status_code == 401
#         assert NO_AUTH_RESPONSE in response.json.values()
#         response = self.client.delete(
#             "http://localhost:5000/api/lawyer/bill/test_bill_company",
#             headers={"Authorization": "Bearer " + create_token(1, "test_lawyer_username", "test_lawyer_email")}
#         )
#         assert response.status_code == 204
#         assert BillModel.query.count() == 0
#
#     # Test Case: #1 - Test that admin cannot access invoice generation route without token.
#     @pytest.mark.invoice
#     def test_admin_access_get_company_invoice_no_token(self):
#         # 1.  admin logs into system
#         baseUrl = "http://localhost:5000/api/admin/"  # the base url.
#         testRoute = "bill/invoice/test_company_bill"  # test route
#         forHeaders = {
#             "Authorization": "Bearer " + ""}  # No token passed.
#         response = self.client.get(baseUrl + testRoute, headers=forHeaders)
#         # the response(GET) from the server should assert to 401 since no token provided.
#         assert response.status_code == 401
#
#     # Test Case #2: - Test that admin cannot access invoice generation route with invalid token.
#     @pytest.mark.invoice
#     def test_admin_access_get_company_invoice_invalid_token(self):
#         # 1. admin logs into system
#         baseUrl = "http://localhost:5000/api/admin/"  # the base url.
#         testRoute = "bill/invoice/test_bill_company"  # test route
#         buffer = "abcdefghijklmnopqrstuvwxyz" + "123456789"
#         t = ''.join(choice(buffer) for i in
#                     range(len(buffer)))  # generate some random strings.
#         invalidToken = create_token(1, "test_lawyer_username", "test_lawyer_email") + t  # entry of more or less token ==> invalid.
#         forHeaders = {
#             "Authorization": "Bearer " + invalidToken}  # headers.
#         response = self.client.get(
#             baseUrl + testRoute,
#             headers=forHeaders)  # @NOTE: headers where not passed.
#         # the response(GET) from the server should assert to 401 since no token provided.
#         assert response.status_code == 401
#
#     # Test Case: #3 - Confirm that admin can access invoice generation route with the valid token provided.
#     @pytest.mark.invoice
#     def test_admin_can_access_get_company_invoice_with_token_provided(
#         self):
#         # 1. admin logs into system.
#         baseUrl = "http://localhost:5000/api/admin/"  # the base url
#         testRoute = "bill/invoice/test_company_bill"  # test route
#         validToken = create_token(1, "test_lawyer_username", "test_lawyer_email")
#         forHeaders = {"Authorization": "Bearer " + validToken}  # headers.
#         # 2. admin's token get passed.
#         response = self.client.get(baseUrl + testRoute, headers=forHeaders)
#         # the response from the server should be successfully since tokens are passed.
#         assert response.status_code == 200 or 201
#
#     # Test Case: #4 - Confirm that admin can generate invoice
#     @pytest.mark.invoice
#     def test_admin_can_generate_invoice(self):
#         # 1. admin logs into system.
#         baseUrl = "http://localhost:5000/api/admin/"  # the base url
#         testRoute = "bill/invoice/<company>"  # test route
#         validToken = create_token(1, "test_lawyer_username", "test_lawyer_email")
#         forHeaders = {"Authorization": "Bearer " + validToken}  # headers.
#
#         # 2. admin's token get passed.
#         response = self.client.get(baseUrl + testRoute,
#                                    headers=forHeaders, )
#         # the response from the server should be successfully since tokens are passed.
#         assert response.status_code == 200 or 201
#
#         # print the invoice generated.
#         return response.json.values()
