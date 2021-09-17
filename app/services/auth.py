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


class AuthService:
    def __next__(self):
        pass

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


