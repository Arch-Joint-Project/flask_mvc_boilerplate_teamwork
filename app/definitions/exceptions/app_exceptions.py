from flask import Response
from flask import json
from sqlalchemy.exc import DBAPIError
from werkzeug.exceptions import HTTPException


class AppExceptionCase(Exception):
    def __init__(self, status_code: int, context):
        self.exception_case = self.__class__.__name__
        self.status_code = status_code
        self.context = context

    def __str__(self):
        return (
            f"<AppException {self.exception_case} - "
            + f"status_code = {self.status_code} - context = {self.context}"
        )


def app_exception_handler(exc: AppExceptionCase):
    if isinstance(exc, AssertionError):
        return Response(
            json.dumps({"app_exception": "AssertionError", "errorMessage": exc}),
            status=500,
        )
    if isinstance(exc, DBAPIError):
        return Response(
            json.dumps(
                {"app_exception": "Database Error", "errorMessage": exc.orig.pgerror}
            ),
            status=400,
        )
    if isinstance(exc, HTTPException):
        return Response(
            json.dumps({"app_exception": "HTTP Error", "errorMessage": exc.description}),
            status=exc.code,
        )

    return Response(
        json.dumps({"app_exception": exc.exception_case, "errorMessage": exc.context}),
        status=exc.status_code,
        mimetype="application/json",
    )


class AppException:
    class OperationError(AppExceptionCase):
        """
        Generic Exception to catch failed operations
        """

        def __init__(self, context):

            status_code = 500
            AppExceptionCase.__init__(self, status_code, context)

    class InternalServerError(AppExceptionCase):
        """
        Generic Exception to catch failed operations
        """

        def __init__(self, context):

            status_code = 500
            AppExceptionCase.__init__(self, status_code, context)

    class ResourceExists(AppExceptionCase):
        """
        Resource Creation Failed Exception
        """

        def __init__(self, context):

            status_code = 400
            AppExceptionCase.__init__(self, status_code, context)

    class ResourceDoesNotExist(AppExceptionCase):
        """
        Resource does not exist
        """

        def __init__(self, context=None):
            status_code = 404
            AppExceptionCase.__init__(self, status_code, context)

    class Unauthorized(AppExceptionCase):
        """
        Unauthorized: Not authorized to perform an operation
        """

        def __init__(self, context=None):
            status_code = 401
            AppExceptionCase.__init__(self, status_code, context)

    class ValidationException(AppExceptionCase):
        """
        ValidationException: Data does not conform to what is required by server
        """

        def __init__(self, context):

            status_code = 400
            AppExceptionCase.__init__(self, status_code, context)

    class KeyCloakAdminException(AppExceptionCase):
        """
                Key Cloak Error. Error with regards to Keycloak authentication
        ≈"""

        def __init__(self, context=None, status_code=400):
            AppExceptionCase.__init__(self, status_code, context)

    class BadRequest(AppExceptionCase):
        """
        Bad Request exception to indicate that that the server cannot or
        will not process the request
        """

        def __init__(self, context=None):
            status_code = 400
            AppExceptionCase.__init__(self, status_code, context)
