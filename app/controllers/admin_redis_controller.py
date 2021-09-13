from app.core.result import Result
from app.core.service_result import ServiceResult
from app.repositories import AdminRedisRepository


class AdminRedisController:
    def __init__(self, admin_redis_repository: AdminRedisRepository):
        self.admin_redis_repository = admin_redis_repository

    def set(self, name, data):
        admin = self.admin_redis_repository.set(name, data)
        return ServiceResult(Result(admin, 200))

    def get(self, name):
        admin = self.admin_redis_repository.get(name)
        return ServiceResult(Result(admin, 201))

    def get_all(self, pattern):
        admin = self.admin_redis_repository.get_all(pattern)
        return ServiceResult(Result(admin, 201))

    def delete(self, name):
        admin = self.admin_redis_repository.delete(name)
        return ServiceResult(Result(admin, 200))
