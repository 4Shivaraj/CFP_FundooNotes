import redis


class RedisService:
    def __init__(self):
        self.redis_cache = redis.Redis(**{"host": '127.0.0.1', "port": 6379})

    def getter(self, key):
        return self.redis_cache.get(key)

    def setter(self, key, value):
        return self.redis_cache.set(key, value)


# if __name__ == '__main__':

#     cache = redis.Redis(**{"host": '127.0.0.1', "port": 6379})
#     # cache.set(2, "one")
#     # cache.set(3, 'frustration')
#     print(cache.keys("*"))
#     print(cache.get(5))
