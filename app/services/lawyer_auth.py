import os
import requests
from app.core.exceptions.app_exceptions import AppException
from app.core.service_interfaces.auth_service_interface import (
    AuthServiceInterface,
)
from app.models import LawyerModel
from app import jw, create_app
from flask import jsonify, make_response, redirect
from flask_jwt_extended import (
    create_refresh_token, create_access_token,
    get_jwt_identity, set_access_cookies, set_refresh_cookies,
    unset_jwt_cookies, unset_access_cookies
)
import requests
from datetime import timedelta


# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jw.user_identity_loader
def user_identity_lookup(lawyer):
    return lawyer.id


# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jw.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return LawyerModel.query.filter_by(id=identity).one_or_none()


# @jw.unauthorized_loader
# def unauthorized_callback(callback):
#     # No auth header
#     return "unauthorized"


# @jw.invalid_token_loader
# def invalid_token_callback(callback):
#     # Invalid Fresh/Non-Fresh Access token in auth header
#     response = jsonify({"invalid": "token"})
#     unset_jwt_cookies(response)
#     return response, 302


# @jw.expired_token_loader
# def expired_token_callback(jwt_header, jwt_payload):
#     # Expired auth header
#     response = requests.get("http://localhost:5000/admin/token/refresh")
#     print(f'this is {response.content}')
#     return response, 302


class AuthService(AuthServiceInterface):
    def get_token(self, request_data):
        pass

    def refresh_token(self, user_data):
        pass

    def create_user(self, request_data):
        pass

    def create_token(self, user_data):
        access_token = create_access_token(identity=user_data, expires_delta=timedelta(hours=10))
        refresh_token = create_refresh_token(identity=user_data)
        response = jsonify(
            {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        )
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        return response, 200


