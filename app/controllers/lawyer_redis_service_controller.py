from app.core.result import Result
from app.core.service_result import ServiceResult
from app.repositories.lawyer_redis_repository import LawyerRedisRepository


class LawyerRedisController:
    def __init__(self,lawyer_redis_repository:LawyerRedisRepository):
        self.lawyer_redis_repository = lawyer_redis_repository

    def set(self,name, data):
        lawyer = self.lawyer_redis_repository.set(name, data)
        return ServiceResult(Result(lawyer, 201))

    def get(self,name):
        lawyer = self.lawyer_redis_repository.get(name)
        return ServiceResult(Result(lawyer, 200))

    def get_all(self,pattern):
        lawyer= self.lawyer_redis_repository.get_all(pattern)
        return ServiceResult(Result(lawyer, 200))

    def delete(self,name):
        lawyer = self.lawyer_redis_repository.delete(name)
        return ServiceResult(Result(lawyer, 200))
