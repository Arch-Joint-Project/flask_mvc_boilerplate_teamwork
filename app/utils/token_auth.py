from functools import wraps
from flask import request, jsonify, make_response
import jwt
import os
from jwt import InvalidTokenError
from config import Config


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
            try:
                data = jwt.decode(token, Config.SECRET_KEY,
                                  algorithms=["HS256"])
            except InvalidTokenError as invalid_token:
                return jsonify({
                    "error": invalid_token.args
                }), 401
            if refresh:
                if data["grant_type"] != "refresh_token":
                    return make_response(jsonify({
                        "status": "error",
                        "error": "refresh token required"
                    }), 401)
            else:
                if data["grant_type"] == "refresh_token":
                    return make_response(jsonify({
                        "status": "error",
                        "error": "access token required"
                    }), 401)
            if data["role"] not in role:
                return make_response(jsonify({
                    "status": "error",
                    "error": "unauthorized user"
                }), 401)
            return f(data, *args, **kwargs)

        return decorated

    return check_token
