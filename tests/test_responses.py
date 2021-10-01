from datetime import date, time


class SharedResponse:
    def signin_invalid_credentials(self):
        return {
            "error": "user verification failure. invalid credentials",
            "status": "error"
        }

    def signin_valid_credentials(self):
        return {
            "access_token": "",
            "refresh_token": ""
        }

    def missing_token_authentication(self):
        return {
            "message": "Token is missing !!"
        }

    def resource_unavailable(self):
        return {
            "app_exception": "NotFoundException",
            "errorMessage": "Resource does not exist"
        }

    def unauthorize_operation(self):
        return {
            "error": "unauthorized user",
            "status": "error"
        }

    def refresh_token_required(self):
        return {
            "error": "refresh token required",
            "status": "error"
        }

    def access_token_required(self):
        return {
            "error": "access token required",
            "status": "error"
        }
