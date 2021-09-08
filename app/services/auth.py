# in-built imports
from functools import wraps
import os
from datetime import datetime, timedelta

# third party imports
import jwt
from flask import request, jsonify

# local imports
from app import db


# function for
def create_token(user):
    token = jwt.encode({
        'id': user["id"],
        'exp': datetime.utcnow() + timedelta(minutes=30)
    },
        os.getenv("SECRET_KEY"),
        algorithm="HS256"
    )
    return token


def decode_token(token):
    decoded_token = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
    return decoded_token


# decorator for verifying the JWT
def token_required(model: db.Model):
    def check_token(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            # jwt is passed in the request header
            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']
            # return 401 if token is not passed
            if not token:
                return jsonify({'message': 'Token is missing !!'}), 401

            try:
                # decoding the payload to fetch the stored details
                data = jwt.decode(token, os.getenv("SECRET_KEY"),
                                  algorithms=["HS256"])
                current_user = model.query \
                    .filter_by(id=data['id']) \
                    .first()
            except:
                return jsonify({
                    'message': 'Token is invalid !!'
                }), 401
            # returns the current logged in users contex to the routes
            return f(current_user, *args, **kwargs)

        return decorated

    return check_token
