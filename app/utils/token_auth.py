from functools import wraps
from flask import request, jsonify, make_response
import jwt
import os
from jwt import InvalidTokenError
from config import Config
from app.services import AuthService
from jwt import InvalidTokenError

auth_service = AuthService()


def token_required(role: list, refresh=False):
    def check_token(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                authorization_info = request.headers.get("Authorization")
                token = authorization_info.split(" ")[1]
            if not token:
                return jsonify({'message': 'Token is missing !!'}), 401
            decoded_token = auth_service.decode_token(token)
            if isinstance(decoded_token, dict):
                token_payload = decoded_token
            else:
                return jsonify({
                        "error": decoded_token
                    }), 401
            check_token_type = auth_service.check_token_type(payload=token_payload,
                                                     refresh_token=refresh)
            if check_token_type:
                return check_token_type
            check_role_type = auth_service.check_access_role(token_payload, access_role=role)
            if check_role_type:
                return check_role_type

            return f(token_payload, *args, **kwargs)

        return decorated

    return check_token
