from functools import wraps
from flask import request, jsonify, make_response
import jwt
import os

from jwt import InvalidTokenError


def token_required(role: list):
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
                data = jwt.decode(token, os.getenv("SECRET_KEY"),
                                  algorithms=["HS256"])
            except InvalidTokenError:
                return jsonify({
                    "message": "Token is invalid !!"
                }), 401
            if data["role"] not in role:
                return make_response(jsonify({
                    "status": "error",
                    "error": "operation unauthorized"
                }), 401)
            return f(data, *args, **kwargs)
        return decorated
    return check_token
