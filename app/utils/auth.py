import os

import jwt
import inspect
from functools import wraps
from flask import request
from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidTokenError,
)

from app.core.exceptions import AppException


def auth_required(authorized_roles=None):
    def authorize_user(func):
        """
        A wrapper to authorize an action using
        :param func: {function} the function to wrap around
        :return:
        """

        @wraps(func)
        def view_wrapper(*args, **kwargs):
            authorization = request.headers.get("Authorization")
            if not authorization:
                raise AppException.ValidationException("Missing authentication token")

            token = authorization.split()[1]
            try:
                key = os.getenv("JWT_PUBLIC_KEY")  # noqa E501
                payload = jwt.decode(
                    token,
                    key=key,
                    algorithms=["HS256", "RS256"],
                    audience="account",
                    issuer=os.getenv("JWT_ISSUER"),
                )  # noqa E501
                available_roles = payload.get("realm_access").get("roles")
                service_name = os.getenv("SERVICE_NAME")
                func_name = service_name + "_" + func.__name__
                access_roles = authorized_roles.split("|")
                access_roles.append(func_name)
                for role in access_roles:
                    if role in available_roles:
                        if "user_id" in inspect.getfullargspec(func).args:
                            kwargs["user_id"] = payload.get(
                                "preferred_username"
                            )  # noqa E501
                        return func(*args, **kwargs)
            except ExpiredSignatureError:
                raise AppException.ExpiredTokenException("Token Expired")
            except InvalidTokenError:
                raise AppException.OperationError("Invalid Token")
            raise AppException.Unauthorized()

        return view_wrapper

    return authorize_user
