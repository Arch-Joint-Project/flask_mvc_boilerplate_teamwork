# local imports
import json

from app.core.repository import SQLBaseRepository
from app.models import LawyerModel
from app.services import RedisService


class LawyerRepository(SQLBaseRepository):

    # class member.
    model = LawyerModel # the model is assigned to a LawyerModel


    def __init__(self, redis_service: RedisService): # make use of redis service
        self.redis_service = redis_service
        super().__init__()

    def create(self, obj_in):
        result = super(LawyerRepository, self).create(obj_in)
        data = json.dumps(result)
        self.redis_service.set(f"lawyer__{result.id}", data)
        return result

    def find(self, query_param):
        current_user_id =  query_param.get("id") # get id key from dictionary passed.
        cached_data = self.redis_service.get(f"lawyer__{current_user_id}")
        # find from redis if cached.
        if cached_data :
            return json.loads(cached_data) #  leave find method and return the cached data as JSON.
        # default to CRUD find from the Parent -> SQLBaseRepository
        result = super(LawyerRepository, self).find(query_param) # call the find in parent.
        return result # return result.


    def find_by_id(self, obj_id: int):
        cached_data = self.redis_service.get(f"lawyer__{obj_id}")
        if not cached_data:
            return super(LawyerRepository, self).find_by_id(obj_id)
        result = json.loads(cached_data)
        return result # return the json string of data from Redis as JSON to service result


