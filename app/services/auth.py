# in-built imports
from functools import wraps
import os
from datetime import datetime, timedelta

# third party imports
import jwt
from flask import request, jsonify, make_response
from werkzeug.security import check_password_hash

# local imports
from app import db
from app.utils import auth


class AuthService:
    def __next__(self):
        pass

    def sign_in(self, auth_info, model: db.Model, role=None):
        if not auth_info or not auth_info["username"] or not auth_info["password"]:
            return jsonify({
                "status": "error",
                "error": "authentication information required"
            })
        user = model.query.filter_by(
            username=auth_info["username"]).first()
        if user is not None and user.verify_password(auth_info["password"]):
            return self.create_token(user.id, role=role)
        return jsonify({
            "status": "error",
            "error": "user verification failure. invalid credentials"
        })

    def create_token(self, id, role=None):
        token = jwt.encode({
            'id': id,
            'role': role,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        },
            os.getenv("SECRET_KEY"),
            algorithm="HS256"
        )
        return token


