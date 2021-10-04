# in-built imports
import os
from datetime import datetime, timedelta

# third party imports
import jwt
from flask import jsonify

# local imports
from app import db


class AuthService:
    def sign_in(self, auth_info, model: db.Model):
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

    def create_token(self, id, role=None):
        payload = {
            'id': id,
            'role': role,
            'exp': datetime.utcnow() + timedelta(days=1),
            'grant_type': 'access_token'
        }
        access_token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")
        payload["grant_type"] = "refresh_token"
        payload["exp"] = datetime.utcnow() + timedelta(days=1)
        refresh_token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")
        return [access_token, refresh_token]
