import os
import json
import redis
from redis.exceptions import RedisError

from app.core.exceptions import HTTPException
from app.core.service_interfaces import CacheServiceInterface


REDIS_SERVER = os.getenv("REDIS_SERVER")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

redis_conn = redis.Redis(host=REDIS_SERVER, port=6379, db=0, password=REDIS_PASSWORD, decode_responses=True)


class RedisService(CacheServiceInterface):
    def set(self, name, data):
        """

        :param name: {string} name of the object you want to set
        :param data: {String} the object you want to set
        :return: {None}
        """
        try:
            redis_conn.set(name, data)
            return True
        except RedisError:
            raise HTTPException(status_code=500, description="Error adding to cache")

    def get(self, name):
        """

        :param name: {string} name of the object you want to get
        :return: {Any}
        """
        try:
            data = redis_conn.get(name)
            if data:
                return json.loads(data)
            return data
        except RedisError:
            raise HTTPException(status_code=500, description="Error getting from cache")

    # def get_all(self, pattern):
    #     """
    #
    #     :param pattern: {string} key pattern to retrieve
    #     :return: {Any}
    #     """
    #     try:
    #         data = redis_conn.keys(pattern)
    #         if data:
    #             cached_data = []
    #             for key in data:
    #                 cached_data.append(self.get(key))
    #             return cached_data
    #         return data
    #     except RedisError:
    #         raise HTTPException(status_code=500, description="Error getting from cache")

    def delete(self, name):
        """
        :param name: {string} name of the object you want to delete
        :return: {Bool}
        """
        try:
            redis_conn.delete(name)
        except RedisError:
            raise HTTPException(status_code=500, description="Error deleting from cache")


"/api/v1/lawyers"
# check if the data exists in redis
# retreive from database
# save in redis

# updates, deletes a lawyer
# check if all lawyers exist in redis
# find the lawyer
# if delete, remove the lawyer from the list
# if update, update the lawyer in list
# save to redis again

# get all lawyers from redis
# append the new object to the list
# save to redis


# for a single lawyer instance
# find if the instance exists
# delete key in redis if exists
# update in database
# save to redis
