# local imports
import dataclasses
import json

from app.core.repository import SQLBaseRepository
from app.models import AdminModel
from app.services import RedisService


class AdminRepository(SQLBaseRepository):
    model=AdminModel

    def __init__(self, redis_service: RedisService):  # make use of redis service
        self.redis_service = redis_service
        super().__init__()

    def create(self, obj_in):
        result = super(AdminRepository, self).create(
            obj_in)  # pass data to CRUD
        data = json.dumps(dataclasses.asdict(result))  # return pass data to json string
        self.redis_service.set(f"admin__{result.id}", data)  # insert into redis
        return result

    def index(self):
        from_crud = super(AdminRepository,self).index()  # all entries from SQL Based Database saved as list.
        cached_data = []  #
        print("outside recovery") # we are outside redis search.
        if len(from_crud) is 0: # recovery options from REDIS FIRST.
             count = 1 # count is 0
             print("inside recovery") # are we inside redis search
             try:
                 while True:
                        redis_key = "admin__" + str(count) # in redis, admin key + the id ==> redis insertion key.
                        redis_data = self.redis_service.get(f"{redis_key}")
                        cached_data.append(redis_data) # then get from REDIS and append in cached data list.
                        count = count + 1 # increase count by one.
                        if redis_data is None:
                           return cached_data  # exit as list of admins -> REDIS Cache database
             except TypeError:
                 return cached_data
        # default to CRUD as usual.
        return from_crud # exit as a list of admins -> SQL Based Database.
