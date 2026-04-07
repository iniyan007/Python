import json
from redis_client import redis_client
from config import CACHE_TTL

def make_cache_key(method, url):
    return f"cache:{method}:{url}"

async def get_cache(method, url):
    key = make_cache_key(method, url)
    data = await redis_client.get(key)
    if data:
        return json.loads(data)
    return None

async def get_cache_with_ttl(method, url):
    key = make_cache_key(method, url)

    data = await redis_client.get(key)
    ttl = await redis_client.ttl(key)

    if data:
        return json.loads(data), ttl

    return None, None


async def set_cache(method, url, response):
    key = make_cache_key(method, url)
    await redis_client.set(key, json.dumps(response), ex=CACHE_TTL)