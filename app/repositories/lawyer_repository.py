# local imports
import json

from app.core.repository import SQLBaseRepository
from app.models import LawyerModel
from app.services import RedisService


class LawyerRepository(SQLBaseRepository):
    model = LawyerModel

    # def __init__(self, redis_service: RedisService):
    #     self.redis_service = redis_service
    #     super().__init__()
    #
    # def create(self, obj_in):
    #     result = super(LawyerRepository, self).create(obj_in)
    #     data = json.dumps(result)
    #     self.redis_service.set(f"lawyer__{result.id}", data)
    #     return result
    #
    # def find_by_id(self, obj_id: int):
    #     cached_data = self.redis_service.get(f"lawyer__{obj_id}")
    #     if not cached_data:
    #         return super(LawyerRepository, self).find_by_id(obj_id)
    #
    #     return self.model(**cached_data)


