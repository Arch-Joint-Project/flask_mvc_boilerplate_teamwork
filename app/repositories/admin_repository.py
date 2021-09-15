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



# def index(self):
#     from_crud = super(AdminRepository,self).index()  # all entries from SQL Based Database saved as list.
#     cached_data = []  #
#     if from_crud is [] or None: # recovery options from REDIS FIRST.
#             redis_key = "admin__"
#             for i in range(len(from_crud)): # we search for each admin model's id from list of AdminModels
#                  redis_key = redis_key + from_crud[i].id # in redis, admin key + the id ==> redis insertion key.
#                  cached_data.append(self.redis_service.get(f"{redis_key}")) # then get from REDIS and append in cached data list.
#             return cached_data # exit as list of admins -> REDIS Cache database.
#     # default to CRUD as usual.
#     return from_crud # exit as a list of admins -> SQL Based Database.
