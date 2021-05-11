import os

import redis


class RedisService:
    redis_conn = redis.Redis(host='redis', port=6379, db=0,
                             password=os.getenv("REDIS_PASSWORD"))

    def set(self, name, data):
        self.redis_conn.set(name, data)
        return True

    def get(self, name):
        return self.redis_conn.get(name)
