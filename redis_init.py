import os
import redis

redis_url = 'redis://localhost:6379/9'

if 'NOTDEV' in os.environ:
    redis_url = 'redis://redis.svc.tools.eqiad1.wikimedia.cloud:6379/0'
elif 'DOCKER' in os.environ:
    redis_url = 'redis://redis:6379/9'

def get_redis_conn():

    rediscl = redis.Redis(host='localhost', port=6379, db=9)


    if 'NOTDEV' in os.environ:
        rediscl = redis.Redis(
            host='redis.svc.tools.eqiad1.wikimedia.cloud',
            port=6379,
            db=0)
    return rediscl

REDIS_KEY_PREFIX = 'mw-toolforge-qpqtool'
