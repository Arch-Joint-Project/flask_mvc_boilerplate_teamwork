import os
import requests
from app.definitions.exceptions.app_exceptions import AppException
from app.definitions.service_interfaces.auth_service_interface import \
    AuthServiceInterface


class AuthService(AuthServiceInterface):

    def get_token(self, request_data):
        data = {
            'grant_type': 'password',
            'client_id': os.getenv('CLIENT_ID'),
            'client_secret': os.getenv('CLIENT_SECRET'),
            'username': request_data['username'],
            'password': request_data['password']
        }

        url = "".join(
            [
                os.getenv("KEYCLOAK_URI"),
                "/auth/realms/",
                os.getenv("REALM"),
                "/protocol/openid-connect/token",
            ]
        )

        response = requests.post(url, data=data)
        if response.status_code != 200:
            raise AppException.KeyCloakAdminException(context={
                "message": "Error in username or password"
            }, status_code=response.status_code)
        tokens_data = response.json()
        result = {
            'tokens': {"access_token": tokens_data['access_token'],
                       "refresh_token": tokens_data['refresh_token'], }
        }

        return result


    def refresh_token(self, refresh_token):
        pass

    def create_user(self, data):
        pass
