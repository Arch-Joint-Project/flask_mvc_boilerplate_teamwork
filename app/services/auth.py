# in-built imports
from functools import wraps
import os
from datetime import datetime, timedelta

# third party imports
import jwt
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash

# local imports
from app import db


def create_token(id, username, email):
    token = jwt.encode({
        'id': id,
        'username': username,
        'email': email,
        'exp': datetime.utcnow() + timedelta(minutes=30)
    },
        os.getenv("SECRET_KEY"),
        algorithm="HS256"
    )
    return token


def decode_token(token):
    decoded_token = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
    return decoded_token


def sign_in(auth_info, model: db.Model):
    if not auth_info or not auth_info["username"] or not auth_info["password"]:
        return jsonify(
            {
                "status": "error",
                "error": "authentication required",
                "msg": "no authentication information provided"
            },
            401,
            {'WWW-Authenticate': 'Basic realm="Login required!"'}
        )
    query_response = model.query.filter_by(username=auth_info["username"]).first()
    if not query_response:
        return make_response(
            {
                "status": "error",
                "error": "user does not exist",
            }
        )
    # lawyer_info = handle_result(query_response, schema=).json
    if check_password_hash(query_response.password, auth_info["password"]):
        token = create_token(query_response.id, query_response.username, query_response.email)
        return make_response(jsonify({'token': token}), 200)
    return make_response(
        {
            "status": "error",
            "error": "verification failure",
            "msg": "could not verify user"
        },
        {
            'WWW-Authenticate': 'Basic realm="Login required!"'
        }
    )


# decorator for verifying the JWT
def token_required(model: db.Model):
    def check_token(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            token = None
            # jwt is passed in the request header
            # if 'Authorization' in request.headers:
            if 'Authorization' in request.headers:
                authorization_info = request.headers.get("Authorization")
                token = authorization_info.split(" ")[1]
            # return 401 if token is not passed
            if not token:
                return jsonify({'message': 'Token is missing !!'}), 401
            try:
                # decoding the payload to fetch the stored details
                data = jwt.decode(token, os.getenv("SECRET_KEY"),
                                  algorithms=["HS256"])
            except:
                return jsonify({
                    'message': 'Token is invalid !!'
                }), 401
            current_user = model.query \
                .filter_by(id=data['id'], username=data['username'], email=data['email']) \
                .first()
            if not current_user:
                return jsonify({
                    'message': 'operation unauthorized !!'
                }), 401
            # returns the current logged in users contex to the routes
            return func(current_user, *args, **kwargs)
        return decorated

    return check_token
