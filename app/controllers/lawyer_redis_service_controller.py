from app.repositories.lawyer_redis_repository import LawyerRedisRepository


class LawyerRedisController:
    def __init__(self,lawyer_redis_repository:LawyerRedisRepository):
        self.lawyer_redis_repository = lawyer_redis_repository


    def set(self,name, data):
        self.lawyer_redis_repository.set(name, data)
        return None

    def get(self,name):
        self.lawyer_redis_repository.get(name)
        return None

    def delete(self,name):
        self.lawyer_redis_repository.delete(name)
        return None
