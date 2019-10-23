import redis, time
pool = redis.ConnectionPool(host='localhost', port=6379,decode_responses=True)
r = redis.Redis(connection_pool=pool)
r.lpush('redis_keys:urls','https://www.aqistudy.cn/historydata/')
