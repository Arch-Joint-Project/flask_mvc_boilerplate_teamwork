# local imports
import json

from app.core.repository import SQLBaseRepository
from app.models import LawyerModel
from app.services import RedisService
from app.schema import LawyerReadSchema

lawyer_schema = LawyerReadSchema()


class LawyerRepository(SQLBaseRepository):
    model = LawyerModel

    def __init__(self, redis_service: RedisService):
        self.redis_service = redis_service
        super().__init__()

    def create(self, obj_in):
        result = super(LawyerRepository, self).create(obj_in)
        lawyer_info = lawyer_schema.dumps(result)
        data = json.dumps(lawyer_info)
        self.redis_service.set(f"lawyer__{result.id}", data)
        return result

    def find_by_id(self, obj_id: int):
        cached_data = self.redis_service.get(f"lawyer__{obj_id}")
        if cached_data:
            return json.loads(cached_data)
        return super(LawyerRepository, self).find_by_id(obj_id)


