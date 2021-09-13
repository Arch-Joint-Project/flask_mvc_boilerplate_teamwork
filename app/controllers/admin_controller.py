from app.core.result import Result
from app.core.service_result import ServiceResult
from app.repositories import AdminRepository
from flask import make_response, jsonify
from werkzeug.security import check_password_hash


class AdminController:
    def __init__(self, admin_repository: AdminRepository):
        self.admin_repository = admin_repository

    def index(self):
        admin = self.admin_repository.index()
        return ServiceResult(Result(admin, 200))

    def create(self, data):
        admin = self.admin_repository.create(data)
        return ServiceResult(Result(admin, 201))

    def find(self, query_param):
        # data is coming from url.
        lawyer = self.admin_repository.find(query_param)
        return ServiceResult(Result(lawyer, 200))

    # basic authentication using username and password in request
    def sign_in(self, auth):
        if not auth or not auth["username"] or not auth["password"]:
            return jsonify(
                {
                    "status": "error",
                    "error": "authentication required",
                    "msg": "no authentication information provided"
                },
                401,
                {'WWW-Authenticate': 'Basic realm="Login required!"'}
            )
        admin_user = self.admin_repository.find({"username": auth["username"]})
        if check_password_hash(admin_user.password, auth["password"]):
            return admin_user
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

