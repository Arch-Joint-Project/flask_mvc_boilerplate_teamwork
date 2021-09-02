from app.core.result import Result
from app.core.service_result import ServiceResult
from app.repositories import LawyerRepository
from werkzeug.security import check_password_hash
from flask import jsonify, make_response
from app.services.lawyer_auth import AuthService
authentication = AuthService()


class LawyerController:
    def __init__(self, lawyer_repository: LawyerRepository):
        self.lawyer_repository = lawyer_repository

    def index(self):
        lawyer = self.lawyer_repository.index()
        return ServiceResult(Result(lawyer, 200))

    def create(self, data):
        lawyer = self.lawyer_repository.create(data)
        return ServiceResult(Result(lawyer, 201))

    def signin(self, auth):
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
        lawyer_user = self.lawyer_repository.find({"username": auth["username"]})
        if check_password_hash(lawyer_user.password, auth["password"]):
            return authentication.create_token(lawyer_user)
        return make_response(
            {
                "status": "error",
                "error": "verification failure",
                "msg": "could not verify user"
            },
            401,
            {
                'WWW-Authenticate': 'Basic realm="Login required!"'
            }
        )

    def find_by_id(self, obj_id):
        lawyer = self.lawyer_repository.find_by_id(obj_id)
        return ServiceResult(Result(lawyer, 200))
