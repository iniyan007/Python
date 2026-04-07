import time
from redis_client import redis_client
from config import RATE_LIMIT, WINDOW

async def is_rate_limited(api_key: str):
    key = f"rate:{api_key}"

    data = await redis_client.hgetall(key)

    now = time.time()

    if not data:
        await redis_client.hset(key, mapping={"tokens": RATE_LIMIT - 1,"last": now})
        await redis_client.expire(key, WINDOW)
        return False, RATE_LIMIT - 1

    tokens = float(data["tokens"])
    last = float(data["last"])

    refill = (now - last) * (RATE_LIMIT / WINDOW)
    tokens = min(RATE_LIMIT, tokens + refill)

    if tokens < 1:
        return True, tokens

    tokens -= 1

    await redis_client.hset(key, mapping={
        "tokens": tokens,
        "last": now
    })

    return False, tokens