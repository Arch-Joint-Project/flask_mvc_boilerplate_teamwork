# in-built imports
import os
from datetime import datetime, timedelta

# third party imports
import jwt
from flask import jsonify, make_response
from jwt import InvalidTokenError

# local imports
from app import db
from config import Config


class AuthService:
    def sign_in(self, auth_info: dict, model: db.Model):
        if not auth_info or not auth_info.get("username") or not auth_info.get("password"):
            return jsonify({
                "status": "error",
                "error": "authentication information required"
            })
        user = model.query.filter_by(
            username=auth_info.get("username")).first()
        if user is not None and user.verify_password(auth_info.get("password")):
            user_token = self.create_token(user.id, role=user.role)
            return jsonify({
                "access_token": user_token[0],
                "refresh_token": user_token[1]
            })
        return jsonify({
            "status": "error",
            "error": "user verification failure. invalid credentials"
        })

    def create_token(self, id: int, role=None):
        payload = {
            'id': id,
            'role': role,
            'exp': datetime.utcnow() + timedelta(days=1),
            'grant_type': 'access_token'
        }
        access_token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
        payload["grant_type"] = "refresh_token"
        payload["exp"] = datetime.utcnow() + timedelta(days=1)
        refresh_token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
        return [access_token, refresh_token]

    def decode_token(self, token: str):
        try:
            decode_token = jwt.decode(token, Config.SECRET_KEY,
                              algorithms=["HS256"])
        except InvalidTokenError as invalid_token:
            return invalid_token.args
        return decode_token

    def check_token_type(self, payload: dict, refresh_token=False):
        if refresh_token:
            if payload["grant_type"] != "refresh_token":
                return make_response(jsonify({
                    "status": "error",
                    "error": "refresh token required"
                }), 401)
        else:
            if payload["grant_type"] == "refresh_token":
                return make_response(jsonify({
                    "status": "error",
                    "error": "access token required"
                }), 401)

    def check_access_role(self, payload: dict, access_role: list):
        if payload["role"] not in access_role:
            return make_response(jsonify({
                "status": "error",
                "error": "unauthorized user"
            }), 401)
